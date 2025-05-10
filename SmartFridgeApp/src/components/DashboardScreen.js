import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button, Card, TextInput } from 'react-native-paper';
import { useAnimatedStyle, animate } from 'react-native-reanimated';

const DashboardScreen = () => {
  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Title title="Fridge Inventory" />
        <Card.Content>
          <TextInput
            label="Item Name"
            style={styles.input}
          />
          <TextInput
            label="Quantity"
            keyboardType="numeric"
            style={styles.input}
          />
          <Button mode="contained" style={styles.button}>
            Add Item
          </Button>
        </Card.Content>
      </Card>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  card: {
    marginBottom: 16,
  },
  input: {
    marginBottom: 12,
  },
  button: {
    marginTop: 8,
  },
});

export default DashboardScreen;