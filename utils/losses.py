import tensorflow as tf


def masked_crossentropy(targets: tf.Tensor, logits: tf.Tensor) -> tf.Tensor:
    crossentropy = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    mask = tf.math.logical_not(tf.math.equal(targets, 0))
    mask = tf.cast(mask, dtype=tf.int32)
    loss = crossentropy(targets, logits, sample_weight=mask)
    return loss


def masked_mean_squared_error(targets: tf.Tensor, logits: tf.Tensor) -> tf.Tensor:
    mse = tf.keras.losses.MeanSquaredError()
    mask = tf.math.logical_not(tf.math.equal(targets, 0))
    mask = tf.cast(mask, dtype=tf.int32)
    mask = tf.reduce_max(mask, axis=-1)
    loss = mse(targets, logits, sample_weight=mask)
    return loss


def masked_binary_crossentropy(targets: tf.Tensor, logits: tf.Tensor) -> tf.Tensor:
    bc = tf.keras.losses.BinaryCrossentropy(reduction='none')
    mask = tf.math.logical_not(tf.math.equal(targets, -1))
    mask = tf.cast(mask, dtype=tf.int32)
    loss_ = bc(targets, logits)
    loss_ *= mask
    return tf.reduce_mean(loss_)


def weighted_sum_losses(targets, pred, loss_functions, coeffs):
    total_loss = 0
    loss_vals = []
    for i in range(len(loss_functions)):
        loss = loss_functions[i](targets[i], pred[i])
        loss_vals.append(loss)
        total_loss += coeffs[i] * loss
    return total_loss, loss_vals