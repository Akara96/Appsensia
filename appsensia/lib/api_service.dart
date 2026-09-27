import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Ganti ho IP Address hosi ita nia laptop (10.0.2.2 ba emulator)
  static const String baseUrl = 'http://10.0.2.2:8000/absensia/api';

  static Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      final data = jsonDecode(response.body);
      
      if (response.statusCode == 200 && data['status'] == 'success') {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('nre', data['data']['nre']);
        await prefs.setString('naran', data['data']['naran']);
        return {'success': true, 'message': 'Login susesu!'};
      }
      
      return {'success': false, 'message': data['message'] ?? 'Login falha!'};
    } catch (e) {
      return {'success': false, 'message': 'Eru koneksaun ba server.'};
    }
  }

  static Future<Map<String, dynamic>> scanQR(String token) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final nre = prefs.getString('nre');

      if (nre == null) {
        return {'success': false, 'message': 'Favór login uluk!'};
      }

      final response = await http.post(
        Uri.parse('$baseUrl/scan/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nre': nre,
          'token': token,
        }),
      );

      final data = jsonDecode(response.body);
      
      if (response.statusCode == 200 && data['status'] == 'success') {
        return {'success': true, 'message': data['message'], 'data': data['data']};
      }
      
      return {'success': false, 'message': data['message'] ?? 'Scan falha!'};
    } catch (e) {
      return {'success': false, 'message': 'Eru koneksaun ba server.'};
    }
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
