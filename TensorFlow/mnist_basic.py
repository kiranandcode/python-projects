from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1],
            strides=[1,2,2,1], padding='SAME')


def feed_dict(train):
    if train: 
        xs, ys = mnist.train.next_batch(100)
        k = 0.5
    else:
        xs, ys = mnist.test.images, mnist.test.labels
        k = 1.0
    return {x:xs, y_: ys, keep_prob: k}

import tensorflow as tf
sess = tf.InteractiveSession()


# building "nodes" for the computation
# none means any size of batch  
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# inputs for the dropout variable
with tf.name_scope('dropout'):
    keep_prob = tf.placeholder(tf.float32)
    tf.summary.scalar('dropout_keep_probability', keep_prob)


# convolutional layers for each 5x5 patch, uses 32 kernels to produce a 32 value vector
# the bias will have to be 32 as well
with tf.name_scope('convolution_1'):
    with tf.name_scope('weights'):
        W_conv1 = weight_variable([5,5,1,32])
        variable_summaries(W_conv1)
    with tf.name_scope('bias'):
        b_conv1 = bias_variable([32])
        variable_summaries(b_conv1)

# reshape the input into a square matrix
x_image = tf.reshape(x, [-1, 28, 28, 1])

# create a convolutional layer, 
with tf.name_scope('convolution_1'):
    with tf.name_scope('Wx_plus_b'):
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
# then pool the input
    h_pool1 = max_pool_2x2(h_conv1)


# 2nd convolutional layer

with tf.name_scope('convolution_2'):
    with tf.name_scope('weights'):
        W_conv2 = weight_variable([5,5,32,64])
        variable_summaries(W_conv2)
    with tf.name_scope('bias'):
        b_conv2 = bias_variable([64])
        variable_summaries(b_conv2)


with tf.name_scope('convolution_2'):
    with tf.name_scope('Wx_plus_b'):
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)


with tf.name_scope('network_layer_1'):
# at this point the image has been reduced to a 7x7 image
    with tf.name_scope('weights'):
        W_fc1 = weight_variable([7*7*64, 1024])
        variable_summaries(W_fc1)
    with tf.name_scope('bias'):
        b_fc1 = bias_variable([1024])
        variable_summaries(b_fc1)

# reshape the input into a flat vector
# pass into a matrix
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
with tf.name_scope('network_layer_1'):
    with tf.name_scope('Wx_plus_b'):
        h_fcl = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    tf.summary.histogram('activations', h_fcl)


# second layer weights

with tf.name_scope('network_layer_2'):
    with tf.name_scope('weights'):
        W_fc2 = weight_variable([1024, 10])
        variable_summaries(W_fc2)
    with tf.name_scope('bias'):
        b_fc2 = bias_variable([10])
        variable_summaries(b_fc2)

# apply dropout
with tf.name_scope('dropout'):
    h_fcl_drop = tf.nn.dropout(h_fcl, keep_prob)

with tf.name_scope('network_layer_2'):
    with tf.name_scope('Wx_plus_b'):
        y_conv = tf.matmul(h_fcl_drop, W_fc2) + b_fc2
    tf.summary.histogram('activations', y_conv)


with tf.name_scope('cross_entropy'):
    diff = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv) 
    with tf.name_scope('total'):
        cross_entropy = tf.reduce_mean(diff)
tf.summary.scalar('cross_entropy', cross_entropy)



with tf.name_scope('train'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)



with tf.Session() as sess:

    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter('./summaries/train', sess.graph)

    test_writer = tf.summary.FileWriter('./summaries/test')


    sess.run(tf.global_variables_initializer())


    for i in range(501):
        if i % 100 == 0:
            summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
            test_writer.add_summary(summary,i)
            print("Step[%s]: Accuracy %s" % (i, acc))
        else:
            summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
            train_writer.add_summary(summary, i)


    print('test accuracy %g' % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob:1.0}))










