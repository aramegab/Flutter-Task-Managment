import 'package:flutter/material.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class TaskProvider with ChangeNotifier {
  List<Task> _tasks = [];
  final ApiService _apiService = ApiService();

  List<Task> get tasks => _tasks;

  Future<void> fetchTasks() async {
    try {
      _tasks = await _apiService.getTasks();
      print('Fetched tasks: $_tasks');
      notifyListeners();
    } catch (e) {
      print('Error fetching tasks: $e');
    }
  }

  Future<void> addTask(Task task) async {
    try {
      final newTask = await _apiService.createTask(task);
      _tasks.add(newTask);
      notifyListeners();
    } catch (e) {
      print('Error adding task: $e');
    }
  }

  Future<void> deleteTask(int id) async {
    try {
      await _apiService.deleteTask(id);
      _tasks.removeWhere((task) => task.id == id);
      notifyListeners();
    } catch (e) {
      print('Error deleting task: $e');
    }
  }

  Future<void> toggleTaskCompletion(int id) async {
    try {
      final task = _tasks.firstWhere((task) => task.id == id);
      final updatedTask = Task(
        id: task.id,
        title: task.title,
        description: task.description,
        completed: !task.completed,
      );
      final result = await _apiService.updateTask(id, updatedTask);
      final index = _tasks.indexWhere((task) => task.id == id);
      _tasks[index] = result;
      notifyListeners();
    } catch (e) {
      print('Error toggling task completion: $e');
    }
  }
}