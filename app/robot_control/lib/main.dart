import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:fluttertoast/fluttertoast.dart';  // Import package toast

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]).then((_) {
    runApp(const RobotControllerApp());
  });
}

class RobotControllerApp extends StatelessWidget {
  const RobotControllerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Robot Controller',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const RobotControlScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class RobotControlScreen extends StatefulWidget {
  const RobotControlScreen({super.key});

  @override
  State<RobotControlScreen> createState() => _RobotControlScreenState();
}

class _RobotControlScreenState extends State<RobotControlScreen> {
  String _status = 'UDP: Đang khởi tạo...';
  RawDatagramSocket? _socket;
  InternetAddress _robotIp = InternetAddress('192.168.4.1');
  int _port = 8888;
  final double _speed = 1.0;

  String _activeButton = '';
  Timer? _holdTimer;

  @override
  void initState() {
    super.initState();
    _initUdp();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  }

  Future<void> _initUdp() async {
    try {
      _socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 0);
      setState(() {
        _status = 'UDP: Đã kết nối đến $_robotIp:$_port';
      });
    } catch (e) {
      setState(() {
        _status = 'UDP: Lỗi: $e';
      });
    }
  }

  void _sendSignal(String cmd, double val) {
    if (_socket == null) return;
    final data = {'cmd': cmd, 'val': val};
    final bytes = utf8.encode(jsonEncode(data));
    try {
      _socket!.send(bytes, _robotIp, _port);
    } catch (_) {}
  }

  @override
  void dispose() {
    _holdTimer?.cancel();
    _socket?.close();
    super.dispose();
  }

  double responsiveSize(double small, double medium, double large) {
    final width = MediaQuery.of(context).size.width;
    if (width < 600) return small;
    if (width < 900) return medium;
    return large;
  }

  Widget _controlButton({
    required String label,
    required IconData? icon,
    required String cmdPrefix,
    required String direction,
    Color baseColor = Colors.blue,
  }) {
    final String cmd = '${cmdPrefix}_$direction';
    final double width = responsiveSize(80, 100, 130);
    final double height = responsiveSize(80, 100, 130);
    final double fontOrIconSize = responsiveSize(32, 40, 50);

    return GestureDetector(
      onTapDown: (_) {
        setState(() => _activeButton = cmd);
        _sendSignal(cmd, _speed);
        _holdTimer = Timer.periodic(const Duration(milliseconds: 50), (_) {
          _sendSignal(cmd, _speed);
        });
      },
      onTapUp: (_) {
        setState(() => _activeButton = '');
        _holdTimer?.cancel();
      },
      onTapCancel: () {  // SỬA LỖI: Bỏ (_) thành ()
        setState(() => _activeButton = '');
        _holdTimer?.cancel();
      },
      child: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          shape: icon != null ? BoxShape.circle : BoxShape.rectangle,
          borderRadius: icon == null ? BorderRadius.circular(12) : null,
          color: _activeButton == cmd ? Colors.green : baseColor,
        ),
        child: Center(
          child: icon != null
              ? Icon(icon, size: fontOrIconSize, color: Colors.white)
              : Text(
                  label,
                  style: TextStyle(color: Colors.white, fontSize: fontOrIconSize * 0.4, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
        ),
      ),
    );
  }

  void _showSettingsDialog() {
    final ipController = TextEditingController(text: _robotIp.address);
    final portController = TextEditingController(text: _port.toString());

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Thay đổi IP và Port'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: ipController,
                decoration: const InputDecoration(labelText: 'IP Address'),
              ),
              TextField(
                controller: portController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'Port'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Hủy'),
            ),
            TextButton(
              onPressed: () {
                try {
                  final newIp = InternetAddress(ipController.text);
                  final newPort = int.parse(portController.text);
                  setState(() {
                    _robotIp = newIp;
                    _port = newPort;
                    _status = 'Cập nhật: $_robotIp:$_port';
                  });
                  _socket?.close();
                  _initUdp();
                  Navigator.pop(context);
                } catch (e) {
                  Fluttertoast.showToast(msg: 'Lỗi: IP/Port không hợp lệ!');
                }
              },
              child: const Text('Lưu'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final double padding = responsiveSize(16, 24, 32);
    final double spacingV = responsiveSize(15, 20, 30);
    final double spacingH = responsiveSize(60, 80, 100);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Điều khiển Robot'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _showSettingsDialog,
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(padding),
          child: Column(
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8)),
                child: Text(
                  _status,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              ),
              SizedBox(height: responsiveSize(20, 30, 40)),

              Expanded(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // === BÊN TRÁI: DI CHUYỂN ROBOT ===
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text('Di Chuyển Robot', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                          SizedBox(height: spacingV),
                          _controlButton(label: '', icon: Icons.keyboard_arrow_up, cmdPrefix: 'robot', direction: 'up'),
                          SizedBox(height: spacingV),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _controlButton(label: '', icon: Icons.keyboard_arrow_left, cmdPrefix: 'robot', direction: 'left'),
                              SizedBox(width: spacingH),
                              _controlButton(label: '', icon: Icons.keyboard_arrow_right, cmdPrefix: 'robot', direction: 'right'),
                            ],
                          ),
                          SizedBox(height: spacingV),
                          _controlButton(label: '', icon: Icons.keyboard_arrow_down, cmdPrefix: 'robot', direction: 'down'),
                        ],
                      ),
                    ),

                    // === GIỮA: ĐIỀU KHIỂN THÙNG ===
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text('Điều Khiển Thùng', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                          SizedBox(height: spacingV),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _controlButton(label: 'Nâng\nTrái', icon: null, cmdPrefix: 'thung', direction: 'tl_up', baseColor: Colors.orange),
                              SizedBox(width: responsiveSize(10, 12, 16)),
                              _controlButton(label: 'Nâng\nPhải', icon: null, cmdPrefix: 'thung', direction: 'tr_up', baseColor: Colors.orange),
                            ],
                          ),
                          SizedBox(height: spacingV),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _controlButton(label: 'Hạ\nTrái', icon: null, cmdPrefix: 'thung', direction: 'tl_down', baseColor: Colors.orange),
                              SizedBox(width: responsiveSize(10, 12, 16)),
                              _controlButton(label: 'Hạ\nPhải', icon: null, cmdPrefix: 'thung', direction: 'tr_down', baseColor: Colors.orange),
                            ],
                          ),
                        ],
                      ),
                    ),

                    // === BÊN PHẢI: CÁNH TAY ROBOT ===
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text('Cánh Tay Robot', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                          SizedBox(height: spacingV),
                          _controlButton(label: '', icon: Icons.keyboard_arrow_up, cmdPrefix: 'arm', direction: 'up'),
                          SizedBox(height: spacingV),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _controlButton(label: '', icon: Icons.keyboard_arrow_left, cmdPrefix: 'arm', direction: 'left'),
                              SizedBox(width: responsiveSize(12, 15, 20)),
                              Column(
                                children: [
                                  _controlButton(label: 'Gắp', icon: null, cmdPrefix: 'grip', direction: 'g', baseColor: Colors.purple),
                                  SizedBox(height: responsiveSize(12, 15, 20)),
                                  _controlButton(label: 'Nhả', icon: null, cmdPrefix: 'grip', direction: 'nha', baseColor: Colors.purple),
                                ],
                              ),
                              SizedBox(width: responsiveSize(12, 15, 20)),
                              _controlButton(label: '', icon: Icons.keyboard_arrow_right, cmdPrefix: 'arm', direction: 'right'),
                            ],
                          ),
                          SizedBox(height: spacingV),
                          _controlButton(label: '', icon: Icons.keyboard_arrow_down, cmdPrefix: 'arm', direction: 'down'),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}