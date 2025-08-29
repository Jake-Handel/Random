"""
A simple implementation of a feedforward neural network with ReLU and softmax activation.
"""

from typing import List, Tuple
import numpy as np


class NeuralNetwork:
    """A simple feedforward neural network implementation.
    
    Attributes:
        layers: List of integers representing the number of neurons in each layer.
        learning_rate: Learning rate for weight updates during training.
        weights: List of weight matrices for each layer.
        biases: List of bias vectors for each layer.
        z_values: List to store pre-activation values during forward pass.
        a_values: List to store post-activation values during forward pass.
    """

    def __init__(self, layers: List[int], learning_rate: float = 0.01) -> None:
        """Initialize the neural network with given architecture.
        
        Args:
            layers: List containing the number of neurons in each layer.
                   Example: [input_dim, hidden1, hidden2, output_dim]
            learning_rate: Step size for updating weights during training.
        """
        self.layers = layers
        self.learning_rate = learning_rate
        self.weights: List[np.ndarray] = []
        self.biases: List[np.ndarray] = []
        self.z_values: List[np.ndarray] = []
        self.a_values: List[np.ndarray] = []
        self.initialize_weights()

    def initialize_weights(self) -> None:
        """Initialize weights and biases using random values from a normal distribution."""
        for i in range(len(self.layers) - 1):
            # He initialization for ReLU
            std_dev = np.sqrt(2.0 / self.layers[i])
            weight = np.random.randn(self.layers[i], self.layers[i + 1]) * std_dev
            bias = np.zeros((1, self.layers[i + 1]))
            self.weights.append(weight)
            self.biases.append(bias)

    @staticmethod
    def activation(z: np.ndarray) -> np.ndarray:
        """ReLU activation function.
        
        Args:
            z: Input array.
            
        Returns:
            Element-wise ReLU of input: max(0, z)
        """
        return np.maximum(0, z)

    @staticmethod
    def activation_derivative(z: np.ndarray) -> np.ndarray:
        """Derivative of ReLU function.
        
        Args:
            z: Input array.
            
        Returns:
            Element-wise derivative: 1 if z > 0, else 0
        """
        return np.where(z > 0, 1, 0)

    @staticmethod
    def softmax(z: np.ndarray) -> np.ndarray:
        """Softmax activation function for multi-class classification.
        
        Args:
            z: Input array (logits).
            
        Returns:
            Probability distribution over classes.
        """
        # Numerically stable softmax
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / exp_z.sum(axis=1, keepdims=True)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Perform forward propagation through the network.
        
        Args:
            X: Input data of shape (n_samples, n_features).
            
        Returns:
            Output of the network after forward pass.
        """
        self.z_values = []  # Reset z values
        self.a_values = [X]  # Input layer activations
        
        # Forward pass through hidden layers
        for i in range(len(self.weights) - 1):
            z = np.dot(self.a_values[-1], self.weights[i]) + self.biases[i]
            a = self.activation(z)
            self.z_values.append(z)
            self.a_values.append(a)
        
        # Output layer with softmax
        z_output = np.dot(self.a_values[-1], self.weights[-1]) + self.biases[-1]
        a_output = self.softmax(z_output)
        self.z_values.append(z_output)
        self.a_values.append(a_output)
        
        return a_output

    def backward(self, X: np.ndarray, y: np.ndarray) -> None:
        """Perform backpropagation and update weights and biases.
        
        Args:
            X: Input data of shape (n_samples, n_features).
            y: One-hot encoded true labels of shape (n_samples, n_classes).
        """
        m = X.shape[0]  # Number of samples
        
        # Output layer gradient
        dz_output = self.a_values[-1] - y
        dw_output = np.dot(self.a_values[-2].T, dz_output) / m
        db_output = np.sum(dz_output, axis=0, keepdims=True) / m
        
        # Update output layer parameters
        self.weights[-1] -= self.learning_rate * dw_output
        self.biases[-1] -= self.learning_rate * db_output
        
        # Backpropagate through hidden layers
        da = dz_output
        for i in reversed(range(len(self.weights) - 1)):
            dz = da.dot(self.weights[i + 1].T) * self.activation_derivative(self.z_values[i])
            dw = np.dot(self.a_values[i].T, dz) / m
            db = np.sum(dz, axis=0, keepdims=True) / m
            
            # Update parameters
            self.weights[i] -= self.learning_rate * dw
            self.biases[i] -= self.learning_rate * db
            
            # Prepare for next layer
            da = dz

    @staticmethod
    def compute_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute cross-entropy loss.
        
        Args:
            y_true: One-hot encoded true labels.
            y_pred: Predicted probabilities.
            
        Returns:
            Cross-entropy loss value.
        """
        m = y_true.shape[0]
        # Add small epsilon to avoid log(0)
        loss = -np.sum(y_true * np.log(y_pred + 1e-8)) / m
        return loss

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000) -> None:
        """Train the neural network.
        
        Args:
            X: Training data of shape (n_samples, n_features).
            y: One-hot encoded training labels of shape (n_samples, n_classes).
            epochs: Number of training iterations over the entire dataset.
        """
        for epoch in range(epochs):
            # Forward and backward pass
            y_pred = self.forward(X)
            self.backward(X, y)
            
            # Print training progress
            if epoch % 100 == 0:
                loss = self.compute_loss(y, y_pred)
                print(f'Epoch {epoch:4d}, Loss: {loss:.6f}')

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make class predictions for input data.
        
        Args:
            X: Input data of shape (n_samples, n_features).
            
        Returns:
            Predicted class indices of shape (n_samples,).
        """
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)


def create_sample_data(n_samples: int = 100, n_features: int = 4, n_classes: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """Create sample training data.
    
    Args:
        n_samples: Number of samples to generate.
        n_features: Number of features per sample.
        n_classes: Number of output classes.
        
    Returns:
        Tuple of (X, y) where X is the input data and y is one-hot encoded labels.
    """
    np.random.seed(42)
    X = np.random.rand(n_samples, n_features)
    y = np.zeros((n_samples, n_classes))
    y[np.arange(n_samples), np.random.choice(n_classes, n_samples)] = 1
    return X, y


def main() -> None:
    """Example usage of the NeuralNetwork class."""
    # Generate sample data
    X_train, y_train = create_sample_data(n_samples=1000, n_features=4, n_classes=3)
    
    # Initialize and train the neural network
    nn = NeuralNetwork(layers=[4, 8, 8, 3], learning_rate=0.01)
    print("Starting training...")
    nn.train(X_train, y_train, epochs=1000)
    
    # Make predictions on new data
    X_test, _ = create_sample_data(n_samples=5, n_features=4, n_classes=3)
    predictions = nn.predict(X_test)
    print("\nSample predictions:", predictions)


if __name__ == "__main__":
    main()
