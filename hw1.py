import math

def remove_unknowns(r1, r2):
    new_list1 = []
    new_list2 = []
    for i in range(0, len(r1)):
        if math.isnan(r1[i]) or math.isnan(r2[i]):
            continue
        else:
            new_list1.append(r1[i])
            new_list2.append(r2[i])

    # nan_value1 = sum(r1) / len(r1)
    # nan_value2 = sum(r2) / len(r2)

    return new_list1, new_list2, (len(r1) - len(new_list1))

def manhattan_dist(r1, r2):
    if len(r1) == 0 or len(r2) == 0:
        print("r1 or r2 are empty")
    elif len(r1) != len(r2):
        print("vectors are not the same length")
    else:
        l1, l2, num_of_nan = remove_unknowns(r1, r2)
        if len(l1) == 0:
            return float('nan')
        else:
            distance = 0
            for i in range(0, len(l1)):    
                distance += abs(l1[i] - l2[i])

            avg_dist = distance / len(l1)
            return distance + (num_of_nan * avg_dist)

def euclidean_dist(r1, r2):
    if len(r1) == 0 or len(r2) == 0:
        print("r1 or r2 are empty")
    elif len(r1) != len(r2):
        print("vectors are not the same length")
    else:
        l1, l2, num_of_nan = remove_unknowns(r1, r2)
        if len(l1) == 0:
            return float('nan')
        else:
            distance = 0
            for i in range(0, len(l1)):
                distance += (l1[i] - l2[i]) ** 2

            avg_dist = distance / len(l1)
            return math.sqrt(distance  + (num_of_nan * avg_dist))



def single_linkage(c1, c2, distance_fn):
    """ Arguments c1 and c2 are lists of lists of numbers
    (lists of input vectors or rows).
    Argument distance_fn is a function that can compute
    a distance between two vectors (like manhattan_dist)."""
    final_distance = float('nan')
    counter = 0
    for r1 in c1:
        for r2 in c2:
            distance = distance_fn(r1, r2)
            if math.isnan(distance):
                continue
            else:  
                if counter == 0:
                    final_distance = distance
                    counter += 1
                elif distance <= final_distance:
                    final_distance = distance
    return final_distance


def complete_linkage(c1, c2, distance_fn):
    final_distance = float('nan')
    counter = 0
    for r1 in c1:
        for r2 in c2:
            distance = distance_fn(r1, r2)
            if math.isnan(distance):
                continue
            else:  
                if counter == 0:
                    final_distance = distance
                    counter += 1
                elif distance >= final_distance:
                    final_distance = distance
    return final_distance

# [[NAN], [1]], [[NAN]]
def average_linkage(c1, c2, distance_fn):
    final_distance = -1
    num = 0
    flag = True
    for r1 in c1:
        for r2 in c2:
            distance = distance_fn(r1, r2)
            if math.isnan(distance):
                num += 1
                continue
            else:  
                if flag:
                    final_distance = 0
                    flag = False
                final_distance += distance

    # leave out vectors that include NAN
    normalize = (len(c1) * len(c2)) - num
    # print(normalize)            
    if final_distance == -1:
        return float('nan')
    else:
        return (final_distance / normalize)


# [[['Cene'], ['Leon']], ['Franci']]
def unpack_cluster(cluster):
    unpacked = []
    for item in cluster:
        if isinstance(item, list):
            unpacked.extend(unpack_cluster(item))
        else:
            unpacked.append(item)
    return unpacked


class HierarchicalClustering:

    def __init__(self, cluster_dist, return_distances=False):
        # the function that measures distances clusters (lists of data vectors)
        self.cluster_dist = cluster_dist

        # if the results of run() also needs to include distances;
        # if true, each joined pair in also described by a distance.
        self.return_distances = return_distances

    def closest_clusters(self, data, clusters):
        """
        Return the closest pair of clusters and their distance.
        """
        final_distance = 0
        cluster_index1 = 0
        cluster_index2 = 0
        counter = 0
        # Loop through clusters
        for i in range(0,len(clusters)):
            for j in range(0, len(clusters)):
                # Avoid comparing the same clusters
                if i != j:
                    cluster1 = unpack_cluster(clusters[i])
                    cluster2 = unpack_cluster(clusters[j])
                    # create empty lists of vectors for each cluster
                    r1 = []
                    r2 = []
                    # fill r1 and r2 with data vectors from each cluster
                    for value1 in cluster1:
                        if isinstance(value1, int) or isinstance(value1, float):
                            continue
                        else:
                            r1.append(data[value1])


                    for value2 in cluster2:
                        if isinstance(value2, int) or isinstance(value2, float):
                            continue
                        else:
                            r2.append(data[value2])

                    # calculate distance between 2 clusters and update variables if needed
                    distance = self.cluster_dist(r1, r2)
                    if math.isnan(distance):
                        continue
                    else:
                        if len(clusters) == 2:
                            return ((clusters[j], clusters[i], distance))
                        elif counter == 0:
                            final_distance = distance
                            counter += 1
                        elif distance <= final_distance:
                            final_distance = distance
                            cluster_index1 = i
                            cluster_index2 = j
        # Check if the final_distance is an integer or a float
        if final_distance.is_integer():
            final_distance = int(final_distance)
        #print((clusters[cluster_index2], clusters[cluster_index1],  final_distance))
        return ((clusters[cluster_index2], clusters[cluster_index1], final_distance))

            

    def run(self, data):
        """
        Performs hierarchical clustering until there is only a single cluster left
        and return a recursive structure of clusters.
        """

        # clusters stores current clustering. It starts as a list of lists
        # of single elements, but then evolves into lists like
        # [[["Albert"], [["Branka"], ["Cene"]]], [["Nika"], ["Polona"]]]
        clusters = [[name] for name in data.keys()]
        while len(clusters) >= 2:
            # print(len(clusters))
            # print(clusters)
            first, second, distance = self.closest_clusters(data, clusters)
            if math.isnan(distance):
                continue
            else:
                for i in range(0, len(clusters)):
                    if clusters[i] == first:
                        if self.return_distances:
                            clusters[i] = [first, second, distance]
                        else:
                            clusters[i] = [first, second]
                        break
            clusters.remove(second)
         
        return clusters


if __name__ == "__main__":

    data = {"a": [1, 2],
            "b": [2, 3],
            "c": [5, 5]}

    def average_linkage_w_manhattan(c1, c2):
        return average_linkage(c1, c2, manhattan_dist)

    hc = HierarchicalClustering(cluster_dist=average_linkage_w_manhattan)
    clusters = hc.run(data)
    print(clusters)  # [[['c'], [['a'], ['b']]]] (or equivalent)

    hc = HierarchicalClustering(cluster_dist=average_linkage_w_manhattan,
                                return_distances=True)
    clusters = hc.run(data)
    print(clusters)  # [[['c'], [['a'], ['b'], 2.0], 6.0]] (or equivalent)

