import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import DashboardScreen from '../components/DashboardScreen';
import InventoryList from '../components/InventoryList';
import ItemForm from '../components/ItemForm';

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Dashboard">
      <Stack.Screen 
        name="Dashboard" 
        component={DashboardScreen} 
        options={{ title: 'Dashboard' }} 
      />
      <Stack.Screen 
        name="InventoryList" 
        component={InventoryList} 
        options={{ title: 'Inventory' }} 
      />
      <Stack.Screen 
        name="ItemForm" 
        component={ItemForm} 
        options={{ title: 'Add Item' }} 
      />
    </Stack.Navigator>
  );
};

export default AppNavigator;