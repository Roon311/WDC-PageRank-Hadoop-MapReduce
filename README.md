# Web Link Structure Analysis using MapReduce

## Introduction
The World Wide Web is a vast network of interconnected domains, where hyperlinks serve as the backbone connecting information across different websites. Understanding the link structure of the web is crucial for various applications, including search engine optimization, web analytics, and information retrieval. In this project, we leverage the power of MapReduce, a parallel processing framework, to analyze the link structure of the web using the WDC Hyperlink Graphs dataset.

The dataset is represented in the Index/Arc format, consisting of two files: the index file, which provides information about each node (domain), and the arc file, which specifies the directed edges (hyperlinks) between nodes. Our objective is to perform comprehensive analysis on the link relationships within this dataset, specifically focusing on the **outlinks** and **inlinks** of each domain.

## Data Description
### Index File

The `index` file contains information about each node (domain) in the graph. Each line represents a single node, with two columns separated by tabs. The first column provides the node name, and the second column indicates the node index. The nodes are sorted by index, showcasing a total of 106 nodes in the dataset.

```plaintext
| Node Name            | Node Index |
|----------------------|------------|
| 1000notes.com        | 0          |
| 100500.tv            | 1          |
| abebooks.com         | 2          |
| abebooks.de          | 3          |
| amazon-presse.de     | 4          |
| ...                  | ...        |
| amazon.fr            | 12         |
| amazon.it            | 13         |
| angrybirds.com       | 14         |
| animationplayhouse.com| 15         |
```

### Arc File

The `arc` file specifies the directed edges (hyperlinks) between nodes. Each line in this file signifies a directed edge, with two columns denoting the origin and target nodes, respectively. The nodes are sorted by index, resulting in a total of 141 arcs in the dataset.

```plaintext
| Origin Node | Target Node |
|-------------|-------------|
| 7           | 5           |
| 7           | 6           |
| 7           | 8           |
| 7           | 9           |
| 7           | 10          |
| ...         | ...         |
| 10          | 8           |
```

These files collectively represent a graph with 106 nodes and 141 arcs, providing a structured view of the connectivity within the dataset. The data is sorted by index, facilitating efficient analysis and interpretation.

## Setting Up Hadoop and Data Preparation
To begin the Hadoop environment, start the NameNode, DataNode, Secondary NameNode, and the ResourceManager by opening the terminal and entering the following command:

```bash
start-all.sh
```

Once Hadoop is running, create a user directory in the Hadoop Distributed File System (HDFS) using the following commands:

```bash
hadoop fs -mkdir /user
hadoop fs -mkdir /user/hadoopuser
hadoop fs -mkdir /user/hadoopuser/assignment1
```

If you need to remove a folder, you can use:

```bash
hadoop fs -rm -r <path>
```

The user directory is now set up. Next, move to the local source directory and copy the data to HDFS:

```bash
mkdir data
mv example_arcs data/
hadoop fs -copyFromLocal Downloads/data /user/hadoopuser/assignment1
hadoop fs -copyFromLocal Downloads/example_index /user/hadoopuser/assignment1
```

You can visualize the HDFS structure, including the data and example_index folders, by navigating to [Hadoop Explorer](http://localhost:50070/explorer.html#/user/hadoopuser/assignment1).

![hadoopexplorer](https://github.com/Roon311/WDC-PageRank-Hadoop-MapReduce/assets/75309751/bab46189-ab4e-499c-8192-93fd9c083d94)


# MapReduce Implementation

## Mapper: `mapper_wdc.py`
The Mapper script (`mapper_wdc.py`) reads input lines from the standard input (STDIN), representing directed edges in the graph. Each line consists of the origin and target nodes separated by a tab. The script extracts the origin node and prints key-value pairs, where the key is the origin node, and the value is set to 1. This initial step counts the outlinks for each domain.

To validate the Mapper, execute the following command:

```bash
hadoop fs -cat /user/hadoopuser/assignment1/data/* | ./mapper_wdc.py
```

If a permission error is encountered, change the permission of the Mapper script:

```bash
sudo chmod 777 mapper_wdc.py
```

The output of the Mapper should resemble the following:

| Origin Node | Count |
|-------------|-------|
| 7           | 1     |
| 7           | 1     |
| 7           | 1     |
| ...         | ...   |
| 105         | 1     |

Once again, validate the output of the Target Mapper through the following command:

```bash
hadoop fs -cat /user/hadoopuser/assignment1/data/* | ./mapper_target.py
```

The output of the Target Mapper should resemble the following:

| Origin Node | Count |
|-------------|-------|
| 5           | 1     |
| 6           | 1     |
| 9           | 1     |
| ...         | ...   |
| 25          | 1     |

## Reducer: `reducer_wdc.py`
The Reducer script (`reducer_wdc.py`) receives key-value pairs from the Mapper, where the key is the node (domain), and the value is the count of occurrences from the Mapper. The script processes these pairs and accumulates the counts for each node. It takes advantage of Hadoop's sorting of input by key before passing it to the Reducer.

To run the entire MapReduce job and save the output in `dataoutput`, use the following command for Origin (Outlinks):

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
-file /home/hadoopusr/mapper_wdc.py -mapper /home/hadoopusr/mapper_wdc.py \
-file /home/hadoopusr/reducer_wdc.py -reducer /home/hadoopusr/reducer_wdc.py \
-input /user/hadoopuser/assignment1/data/* \
-output /user/hadoopuser/assignment1/dataoutput
```

And for Target (Inlinks):

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
-file /home/hadoopusr/mapper_target.py -mapper /home/hadoopusr/mapper_target.py \
-file /home/hadoopusr/reducer_wdc.py -reducer /home/hadoopusr/reducer_wdc.py \
-input /user/hadoopuser/assignment1/data/* \
-output /user/hadoopuser/assignment1/target_output
```

## Block Diagram
The following block diagram illustrates the MapReduce process for both Origin (Outlinks) and Target (Inlinks), showcasing the data flow and processing steps.

![blockDiagramSequence](https://github.com/Roon311/WDC-PageRank-Hadoop-MapReduce/assets/75309751/13c653fd-dd77-417f-91af-3092a6df80db)

# MapReduce for Join

## Mapper_join Explanation
The `mapper_join.py` processes input data and extracts link ID, link, and sum result. If the key is a digit, it is considered a link ID, and the link is set to '-'. If the key is not a digit, it is considered a link, and the link ID is set to '-'. The output includes link ID, link, and sum result.

## Reducer_join Explanation
The `reducer_join.py` sorts the records based on the key and processes them sequentially. It accumulates the sum results for the same key and outputs the final results, including the link and sum. Then we sort the output based on the count before returning it.

To run the MapReduce job for outlinks and save the output in `joined_output`, use the following command:

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
-files /home/hadoopusr/mapper_join.py,/home/hadoopusr/reducer_join.py \
-mapper "/usr/bin/env python3 mapper_join.py" \
-reducer "/usr/bin/env python3 reducer_join.py" \
-input /user/hadoopuser/assignment1/dataoutput/part-* /user/hadoopuser/assignment1/example_index \
-output /user/hadoopuser/assignment1/joined_output
```

To run the MapReduce job for inlinks and save the output in `joined_target_output`, use the following command:

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
-files /home/hadoopusr/mapper_join.py,/home/hadoopusr/reducer_join.py \
-mapper "/usr/bin/env python3 mapper_join.py" \
-reducer "/usr/bin/env python3 reducer_join.py" \
-input /user/hadoopuser/assignment1/target_output/part-* /user/hadoopuser/assignment1/example_index \
-output /user/hadoopuser/assignment1/joined_target_output
```

Now, you can check the Hadoop Explorer at [http://localhost:50070/explorer.html#/user/hadoopuser/assignment1](http://localhost:50070/explorer.html#/user/hadoopuser/assignment1) to view the output folders.
![hadoopexplorer2](https://github.com/Roon311/WDC-PageRank-Hadoop-MapReduce/assets/75309751/846149e3-b2a0-4159-b23c-24376203e4f4)


## Analysis based on the Joined Tables
Now, let's answer the questions based on the joined tables:

- **How many outlinks does every domain have?**: [Check the joined_output table]
- **How many inlinks does every domain have?**: [Check the joined_target_output table]
- **Which domain has the most outlinks?**: `amazon.com`
- **Which domain has the most inlinks?**: `blogspot.com`



Kindly refer to the pdf documentation for thorough details.
