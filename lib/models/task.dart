class Task {
  final int? id; // Added id field
  final String title;
  final String? description;
  final bool completed;

  Task({this.id, required this.title, this.description, required this.completed});

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      completed: json['completed'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'completed': completed,
    };
  }

  @override
  String toString() => 'Task(id: $id, title: $title, description: $description, completed: $completed)';
}