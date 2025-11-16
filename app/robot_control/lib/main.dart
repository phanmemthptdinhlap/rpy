import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:fluttertoast/fluttertoast.dart';

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
  String _laststatus = 'Chưa gửi dữ liệu';
  RawDatagramSocket? _socket;
  InternetAddress _robotIp = InternetAddress('192.168.4.1');
  int _port = 8888;
  
  // Loại bỏ _speed = 1.0 vì chúng ta sẽ dùng 1 (int)
  
  // === CẬP NHẬT: Dùng Map<String, int> (1: Bật, 0: Tắt) để tiết kiệm dữ liệu ===
  final Map<String, int> _activeCommands = {
    // Robot Movement
    'robot_up': 0, 'robot_down': 0, 
    'robot_left': 0, 'robot_right': 0,
  
    // Arm
    'arm_up': 0, 'arm_down': 0, 
    'arm_left': 0, 'arm_right': 0,
    'arm_far': 0, 'arm_near': 0,
    // Arm Gap/Nha
    'arm_gap': 0, 'arm_nha': 0,
      // Bucket/Thùng
    'thung_tl_up': 0, 'thung_tr_up': 0, 
    'thung_tl_down': 0, 'thung_tr_down': 0,
  };
  
  Timer? _sendTimer; // Sử dụng một Timer duy nhất để gửi toàn bộ trạng thái

  // Biến tạm thời chỉ để tô màu nút (không cần thiết cho logic gửi data)
  String _activeButton = ''; 

  @override
  void initState() {
    super.initState();
    _initUdp();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  }

  Future<void> _initUdp() async {
    try {
      // Bind to an available port (0) on any IPv4 interface
      _socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 0);
      setState(() {
        _status = 'UDP: Đã kết nối đến $_robotIp:$_port';
      });
      // BẮT ĐẦU: KHỞI TẠO TIMER GỬI DỮ LIỆU LIÊN TỤC
      // Gửi toàn bộ trạng thái 20 lần mỗi giây (50ms)
      _sendTimer = Timer.periodic(const Duration(milliseconds: 50), (_) {
        _sendAllCommands();
      });
      // KẾT THÚC: KHỞI TẠO TIMER
    } catch (e) {
      setState(() {
        _status = 'UDP: Lỗi: $e';
      });
    }
  }

  // === Hàm log kiểm soát lỗi ===
  void _logError(String message) {
    print(message);
  }

  // === HÀM GỬI TOÀN BỘ TRẠNG THÁI NÚT ===
  void _sendAllCommands() {
    if (_socket == null) return;
    
    // Gửi toàn bộ _activeCommands Map dưới dạng JSON.
    final List<int> vals = _activeCommands.map((key, value) => MapEntry(key, value)).values.toList();
    final bytes = utf8.encode(jsonEncode(vals));
    try {
      _socket!.send(bytes, _robotIp, _port);
      _logError('Đang gửi: $vals');
      setState(() {
        _laststatus = ' ${jsonEncode(vals)}';
      });
    } catch (_) {
      // Bỏ qua lỗi gửi tín hiệu (ví dụ: mất kết nối Wi-Fi)
    }
  }

  // === CẬP NHẬT: Dùng int cho trạng thái (1 hoặc 0) ===
  void _updateCommandStatus(String cmd, int val) {
    _activeCommands[cmd] = val;
    // Có thể gọi _sendAllCommands() ở đây một lần để phản hồi nhanh hơn ngay khi trạng thái thay đổi:
    // _sendAllCommands(); 
  }

  @override
  void dispose() {
    _sendTimer?.cancel(); // Hủy Timer gửi data
    _socket?.close();
    super.dispose();
  }

  // === RESPONSIVE: Điều chỉnh kích thước để vừa màn hình nhỏ hơn ===
  double responsiveSize(double small, double medium, double large) {
    // Lấy chiều rộng màn hình hiện tại
    final width = MediaQuery.of(context).size.width;
    // Tùy chỉnh các breakpoint để tối ưu cho landscape mode trên thiết bị nhỏ
    if (width < 600) return small;
    if (width < 900) return medium;
    return large;
  }

  double buttonSize() {
    return responsiveSize(65, 90, 120);
  }
  double buttonIconSize() {
    return responsiveSize(30, 50, 90);
  }
  double buttonFontSize() {
    return responsiveSize(12, 16, 20);
  }

  // === HÀM TẠO KHOẢNG TRỐNG BẰNG NÚT BẤN ===
  Widget _spacerButton() {
    final double size = buttonSize();
    return SizedBox(width: size, height: size);
  }


  // === NÚT ĐIỀU KHIỂN CHUNG (TRÒN / CHỮ) ===
  Widget _controlButton({
    required String label,
    required IconData? icon,
    required String cmdPrefix,
    required String direction,
    Color baseColor = Colors.blue,
    bool isCircle = true,
  }) {
    final String cmd = '${cmdPrefix}_$direction';
    // Đã giảm kích thước nút nhỏ nhất từ 80 xuống 65
    final double size = buttonSize();
    // Đã giảm kích thước icon nhỏ nhất từ 36 xuống 30
    final double iconSize = buttonIconSize();
    // Đã giảm kích thước font nhỏ nhất từ 13 xuống 11
    final double fontSize = buttonFontSize();

    return GestureDetector(
      onTapDown: (_) {
        setState(() => _activeButton = cmd);
        // CẬP NHẬT: Lưu trạng thái nút BẤM (1)
        _updateCommandStatus(cmd, 1);
      },
      onTapUp: (_) {
        setState(() => _activeButton = '');
        // CẬP NHẬT: Lưu trạng thái nút NHẢ (0)
        _updateCommandStatus(cmd, 0);
      },
      onTapCancel: () {
        setState(() => _activeButton = '');
        // CẬP NHẬT: Lưu trạng thái nút NHẢ (0)
        _updateCommandStatus(cmd, 0);
      },
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: isCircle ? BoxShape.circle : BoxShape.rectangle,
          borderRadius: !isCircle ? BorderRadius.circular(12) : null,
          color: _activeButton == cmd ? Colors.green : baseColor,
        ),
        child: Center(
          child: icon != null
              ? Icon(icon, size: iconSize, color: Colors.white)
              : Text(
                  label,
                  style: TextStyle(color: Colors.white, fontSize: fontSize, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
        ),
      ),
    );
  }

  // === DIALOG CÀI ĐẶT IP/PORT ===
  void _showSettingsDialog() {
    final ipController = TextEditingController(text: _robotIp.address);
    final portController = TextEditingController(text: _port.toString());

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Thay đổi IP và Port'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: ipController, decoration: const InputDecoration(labelText: 'IP Address')),
            TextField(controller: portController, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Port')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Hủy')),
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
                // Dừng Timer và khởi tạo lại UDP/Timer
                _sendTimer?.cancel();
                _socket?.close();
                _initUdp();
                Navigator.pop(context);
              } catch (e) {
                // Thay thế Fluttertoast bằng SnackBar hoặc Dialog nếu không muốn dùng thư viện ngoài
                Fluttertoast.showToast(msg: 'Lỗi: IP/Port không hợp lệ!');
              }
            },
            child: const Text('Lưu'),
          ),
        ],
      ),
    );
  }

  // === CÁC CỘT CHÍNH ===
  Widget _buildMovementColumn(double spacingV, double spacingH) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _spacerButton(),
            _controlButton(label: '', icon: Icons.keyboard_arrow_up, cmdPrefix: 'robot', direction: 'up'),
            _controlButton(label: 'Gắp', icon:null, cmdPrefix: 'arm', direction: 'gap', baseColor: Colors.deepPurple),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _controlButton(label: '', icon: Icons.keyboard_arrow_left, cmdPrefix: 'robot', direction: 'left'),
            SizedBox(width: spacingH), // Khoảng cách giữa nút Trái và Phải
            _controlButton(label: '', icon: Icons.keyboard_arrow_right, cmdPrefix: 'robot', direction: 'right'),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _spacerButton(),
            _controlButton(label: '', icon: Icons.keyboard_arrow_down, cmdPrefix: 'robot', direction: 'down'),
            _controlButton(label: 'Nhả', icon:null, cmdPrefix: 'arm', direction: 'nha', baseColor: Colors.deepPurple),
          ],
        ),
      ],
    );
  }

  Widget _buildBucketColumn(double spacingV) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text( _laststatus , style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        SizedBox(height: spacingV),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _controlButton(label: 'Trái', icon: Icons.keyboard_arrow_up, cmdPrefix: 'thung', direction: 'tl_up', baseColor: Colors.orange),
            SizedBox(width: responsiveSize(8, 10, 12)),
            _controlButton(label: 'Phải', icon: Icons.keyboard_arrow_up, cmdPrefix: 'thung', direction: 'tr_up', baseColor: Colors.orange),
          ],
        ),
        SizedBox(height: spacingV),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _controlButton(label: 'Trái', icon: Icons.keyboard_arrow_down, cmdPrefix: 'thung', direction: 'tl_down', baseColor: Colors.orange),
            SizedBox(width: responsiveSize(8, 10, 12)),
            _controlButton(label: 'Phải', icon: Icons.keyboard_arrow_down, cmdPrefix: 'thung', direction: 'tr_down', baseColor: Colors.orange),
          ],
        ),
      ],
    );
  }

  Widget _buildArmColumn(double spacingV, double spacingH) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _controlButton(label: '', icon: Icons.arrow_circle_up, cmdPrefix: 'arm', direction: 'far', baseColor: Colors.purple),
            _controlButton(label: '', icon: Icons.swipe_up, cmdPrefix: 'arm', direction: 'up', baseColor: Colors.deepPurple),
            _spacerButton(),
          ],
        ),
        SizedBox(height: spacingV),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _controlButton(label: '', icon: Icons.swipe_left, cmdPrefix: 'arm', direction: 'left', baseColor: Colors.deepPurple),
            SizedBox(width: spacingH), // Khoảng cách giữa nút Trái và Phải
            _controlButton(label: '', icon: Icons.swipe_right, cmdPrefix: 'arm', direction: 'right', baseColor: Colors.deepPurple),
          ],
        ),
        SizedBox(height: spacingV),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _controlButton(label: '', icon: Icons.arrow_circle_down, cmdPrefix: 'arm', direction: 'near', baseColor: Colors.purple),
            _controlButton(label: '', icon: Icons.swipe_down, cmdPrefix: 'arm', direction: 'down', baseColor: Colors.deepPurple),
            _spacerButton(),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    // Đã giảm padding nhỏ nhất từ 12 xuống 8
    final double padding = responsiveSize(5, 10, 20);
    // Đã giảm khoảng cách dọc nhỏ nhất từ 12 xuống 10
    final double spacingV = responsiveSize(10, 14, 18);
    // Đã giảm khoảng cách ngang nhỏ nhất (giữa nút trái/phải) từ 50 xuống 20
    final double spacingH = responsiveSize(10, 15, 20);

    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            // === LAYOUT CHÍNH ===
            Padding(
              padding: EdgeInsets.all(padding),
              child: Column(
                children: [
                  // Trạng thái + Settings
                  Container(
                    width: double.infinity,
                    decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8)),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Text(_status, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15), overflow: TextOverflow.ellipsis),
                        ),
                        IconButton(icon: const Icon(Icons.settings, size: 24), onPressed: _showSettingsDialog, tooltip: 'Cài đặt'),
                      ],
                    ),
                  ),
                  Expanded(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      // Sử dụng Expanded cho 3 cột để chúng chiếm đều không gian còn lại
                      children: [
                        Expanded(child: _buildMovementColumn(spacingV, spacingH)),
                        Expanded(child: _buildBucketColumn(spacingV)),
                        Expanded(child: _buildArmColumn(spacingV, spacingH)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}