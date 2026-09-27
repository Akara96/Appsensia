import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:appsensia/login_screen.dart';
import 'package:appsensia/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  final prefs = await SharedPreferences.getInstance();
  final hasSession = prefs.getString('nre') != null;

  runApp(MyApp(hasSession: hasSession));
}

class MyApp extends StatelessWidget {
  final bool hasSession;
  const MyApp({super.key, required this.hasSession});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Appsensia FECT',
      theme: ThemeData(
        fontFamily: 'Inter',
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueAccent),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      home: hasSession ? const HomeScreen() : const LoginScreen(),
    );
  }
}
