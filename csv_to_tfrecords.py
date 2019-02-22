"""
function:将（256*8）*nan的tick.csv转化为tfrecords
"""


import tensorflow as tf
import os


input_len = 256


def convert_to_tf(input_filename, output_filename):
    print("Start to convert {} to {}".format(input_filename, output_filename))
    writer = tf.python_io.TFRecordWriter(output_filename)

    for line in open(input_filename, "r"):
        data = line.split(',')
        label = int(float(data[-1][:-1]))
        features = [float(i) for i in data[:-1]]
        example = tf.train.Example(features=tf.train.Features(
            feature={
                "label":
                    tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
                "features":
                    tf.train.Feature(float_list=tf.train.FloatList(value=features)),
            }))
        writer.write(example.SerializeToString())

    writer.close()
    print("Successfully convert {} to {}".format(input_filename, output_filename))


def main():
  current_path = os.getcwd()
  for filename in os.listdir(current_path):
    if filename.endswith(".csv"):
      convert_to_tf(filename, filename + ".tfrecords")


if __name__ == "__main__":
  main()

