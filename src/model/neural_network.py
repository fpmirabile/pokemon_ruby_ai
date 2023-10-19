import tensorflow as tf

def create_model(input_shape, state_shape, num_actions):
    image_input = tf.keras.layers.Input(shape=input_shape)
    state_input = tf.keras.layers.Input(shape=state_shape)

    conv1 = tf.keras.layers.Conv2D(32, (8, 8), strides=(4, 4), activation='relu')(image_input)
    conv2 = tf.keras.layers.Conv2D(64, (4, 4), strides=(2, 2), activation='relu')(conv1)
    conv3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu')(conv2)
    conv_flatten = tf.keras.layers.Flatten()(conv3)

    state_dense = tf.keras.layers.Dense(64, activation='relu')(state_input)

    combined = tf.keras.layers.Concatenate()([conv_flatten, state_dense])
    dense1 = tf.keras.layers.Dense(512, activation='relu')(combined)
    output = tf.keras.layers.Dense(num_actions, activation='linear')(dense1)

    model = tf.keras.Model(inputs=[image_input, state_input], outputs=[output])
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse')

    return model
