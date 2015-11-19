# Import data
# input_data.py is copied from https://github.com/tensorflow/tensorflow/blob/master/tensorflow/g3doc/tutorials/mnist/input_data.py
from lib import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

import tensorflow as tf
sess = tf.InteractiveSession()

# Create the model
x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784,10]), name="W")
b = tf.Variable(tf.zeros([10]), name="b")
y = tf.nn.softmax(tf.matmul(x,W) + b)
saver = tf.train.Saver()

# Define loss and optimizer
y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# Train
tf.initialize_all_variables().run()
for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  train_step.run({x: batch_xs, y_: batch_ys})

save_path = saver.save(sess, "data/softmax-1000.ckpt")
print "Model saved in file: ", save_path

# Test trained model
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))
