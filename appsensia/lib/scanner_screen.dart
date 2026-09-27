import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:appsensia/api_service.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  MobileScannerController cameraController = MobileScannerController();
  bool _isScanning = true;
  bool _isProcessing = false;

  void _onDetect(BarcodeCapture capture) async {
    if (!_isScanning || _isProcessing) return;

    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isNotEmpty) {
      final String? code = barcodes.first.rawValue;
      if (code != null) {
        setState(() {
          _isScanning = false;
          _isProcessing = true;
        });

        // Husu API
        final result = await ApiService.scanQR(code);

        if (mounted) {
          if (result['success']) {
            _showSuccessDialog(result['message'], result['data']);
          } else {
            _showErrorDialog(result['message']);
          }
        }
      }
    }
  }

  void _showSuccessDialog(String message, Map<String, dynamic> data) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Icon(Icons.check_circle, color: Colors.greenAccent, size: 60),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              message,
              style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            Text(
              "Kadeira: ${data['kadeira']}",
              style: const TextStyle(color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            Text(
              "Dosente: ${data['dosente']}",
              style: const TextStyle(color: Colors.grey),
              textAlign: TextAlign.center,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Tutup dialog
              Navigator.pop(context); // Fila ba home
            },
            child: const Text('OK', style: TextStyle(color: Colors.blueAccent, fontSize: 16)),
          ),
        ],
      ),
    );
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Icon(Icons.error_outline, color: Colors.redAccent, size: 60),
        content: Text(
          message,
          style: const TextStyle(color: Colors.white, fontSize: 18),
          textAlign: TextAlign.center,
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _isScanning = true;
                _isProcessing = false;
              });
            },
            child: const Text('Tenta Fali', style: TextStyle(color: Colors.blueAccent, fontSize: 16)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Scan QR Code', style: TextStyle(color: Colors.white)),
        actions: [
          IconButton(
            icon: ValueListenableBuilder(
              valueListenable: cameraController.torchState,
              builder: (context, state, child) {
                switch (state) {
                  case TorchState.off:
                    return const Icon(Icons.flash_off, color: Colors.grey);
                  case TorchState.on:
                    return const Icon(Icons.flash_on, color: Colors.yellow);
                }
              },
            ),
            onPressed: () => cameraController.toggleTorch(),
          ),
          IconButton(
            color: Colors.white,
            icon: ValueListenableBuilder(
              valueListenable: cameraController.cameraFacingState,
              builder: (context, state, child) {
                switch (state) {
                  case CameraFacing.front:
                    return const Icon(Icons.camera_front);
                  case CameraFacing.back:
                    return const Icon(Icons.camera_rear);
                }
              },
            ),
            onPressed: () => cameraController.switchCamera(),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: cameraController,
            onDetect: _onDetect,
          ),
          // Scanner overlay
          Container(
            decoration: ShapeDecoration(
              shape: QrScannerOverlayShape(
                borderColor: Colors.blueAccent,
                borderRadius: 10,
                borderLength: 30,
                borderWidth: 10,
                cutOutSize: MediaQuery.of(context).size.width * 0.8,
              ),
            ),
          ),
          if (_isProcessing)
            Container(
              color: Colors.black54,
              child: const Center(
                child: CircularProgressIndicator(color: Colors.blueAccent),
              ),
            ),
        ],
      ),
    );
  }
}

class QrScannerOverlayShape extends ShapeBorder {
  final Color borderColor;
  final double borderWidth;
  final Color overlayColor;
  final double borderRadius;
  final double borderLength;
  final double cutOutSize;

  const QrScannerOverlayShape({
    this.borderColor = Colors.red,
    this.borderWidth = 3.0,
    this.overlayColor = const Color.fromRGBO(0, 0, 0, 80),
    this.borderRadius = 0,
    this.borderLength = 40,
    this.cutOutSize = 250,
  });

  @override
  EdgeInsetsGeometry get dimensions => const EdgeInsets.all(10);

  @override
  Path getInnerPath(Rect rect, {TextDirection? textDirection}) {
    return Path()
      ..fillType = PathFillType.evenOdd
      ..addPath(getOuterPath(rect), Offset.zero);
  }

  @override
  Path getOuterPath(Rect rect, {TextDirection? textDirection}) {
    Path getLeftTopPath(Rect rect) {
      return Path()
        ..moveTo(rect.left, rect.bottom)
        ..lineTo(rect.left, rect.top)
        ..lineTo(rect.right, rect.top);
    }

    return getLeftTopPath(rect)
      ..lineTo(rect.right, rect.bottom)
      ..lineTo(rect.left, rect.bottom)
      ..lineTo(rect.left, rect.top);
  }

  @override
  void paint(Canvas canvas, Rect rect, {TextDirection? textDirection}) {
    final width = rect.width;
    final borderWidthSize = width / 2;
    final height = rect.height;
    final borderOffset = borderWidth / 2;
    final borderLength = borderLength > cutOutSize / 2 + borderWidthSize ? cutOutSize / 2 + borderOffset : borderLength;
    final cutOutSize = cutOutSize < width ? cutOutSize : width - borderOffset;

    final backgroundPaint = Paint()
      ..color = overlayColor
      ..style = PaintingStyle.fill;

    final borderPaint = Paint()
      ..color = borderColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = borderWidth;

    final boxPaint = Paint()
      ..color = borderColor
      ..style = PaintingStyle.fill
      ..blendMode = BlendMode.dstOut;

    final cutOutRect = Rect.fromLTWH(
      rect.left + width / 2 - cutOutSize / 2 + borderOffset,
      rect.top + height / 2 - cutOutSize / 2 + borderOffset,
      cutOutSize - borderOffset * 2,
      cutOutSize - borderOffset * 2,
    );

    canvas
      ..saveLayer(rect, backgroundPaint)
      ..drawRect(rect, backgroundPaint)
      ..drawRRect(
        RRect.fromRectAndRadius(cutOutRect, Radius.circular(borderRadius)),
        boxPaint,
      )
      ..restore();

    canvas
      // Top left
      ..drawLine(
        Offset(cutOutRect.left, cutOutRect.top),
        Offset(cutOutRect.left + borderLength, cutOutRect.top),
        borderPaint,
      )
      ..drawLine(
        Offset(cutOutRect.left, cutOutRect.top),
        Offset(cutOutRect.left, cutOutRect.top + borderLength),
        borderPaint,
      )
      // Top right
      ..drawLine(
        Offset(cutOutRect.right, cutOutRect.top),
        Offset(cutOutRect.right - borderLength, cutOutRect.top),
        borderPaint,
      )
      ..drawLine(
        Offset(cutOutRect.right, cutOutRect.top),
        Offset(cutOutRect.right, cutOutRect.top + borderLength),
        borderPaint,
      )
      // Bottom right
      ..drawLine(
        Offset(cutOutRect.right, cutOutRect.bottom),
        Offset(cutOutRect.right - borderLength, cutOutRect.bottom),
        borderPaint,
      )
      ..drawLine(
        Offset(cutOutRect.right, cutOutRect.bottom),
        Offset(cutOutRect.right, cutOutRect.bottom - borderLength),
        borderPaint,
      )
      // Bottom left
      ..drawLine(
        Offset(cutOutRect.left, cutOutRect.bottom),
        Offset(cutOutRect.left + borderLength, cutOutRect.bottom),
        borderPaint,
      )
      ..drawLine(
        Offset(cutOutRect.left, cutOutRect.bottom),
        Offset(cutOutRect.left, cutOutRect.bottom - borderLength),
        borderPaint,
      );
  }

  @override
  ShapeBorder scale(double t) {
    return QrScannerOverlayShape(
      borderColor: borderColor,
      borderWidth: borderWidth * t,
      overlayColor: overlayColor,
      borderRadius: borderRadius * t,
      borderLength: borderLength * t,
      cutOutSize: cutOutSize * t,
    );
  }
}
