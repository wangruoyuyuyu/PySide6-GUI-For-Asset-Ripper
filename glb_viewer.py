import sys
import os
import base64
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QProgressBar,
    QApplication,
    QFileDialog,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import Qt, Signal, QThread, QUrl, QTimer
from PySide6.QtGui import QDesktopServices
import requests


class ThreeJSViewerWindow(QWebEngineView):
    """基于Three.js的WebGL渲染窗口，确保全局对象正确初始化"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.page = CustomWebEnginePage(self)
        self.setPage(self.page)

        # 初始化Three.js页面
        self.setHtml(
            self.generate_threejs_page(),
            baseUrl=QUrl.fromLocalFile(os.getcwd()).toString() + "/",
        )

        # 初始化状态
        self.light_intensity = 0.8
        self.ambient_intensity = 0.3
        self.initialized = False  # 标记JS环境是否初始化完成

        # 等待页面加载完成后验证初始化状态
        self.page.loadFinished.connect(self._on_page_loaded)

    def _on_page_loaded(self, success):
        """页面加载完成后验证初始化状态"""
        if success:
            # 检查threeViewer是否已正确初始化
            self.page.runJavaScript(
                """
                if (window.threeViewer && typeof window.threeViewer.loadGLB === 'function') {
                    true;
                } else {
                    // 尝试重新初始化命名空间
                    window.threeViewer = window.threeViewer || {};
                    false;
                }
            """,
                self._verify_initialization,
            )

    def _verify_initialization(self, result):
        """验证JS环境初始化结果"""
        if result:
            self.initialized = True
            print("Three.js环境初始化成功")
        else:
            print("Three.js环境初始化失败，将在1秒后重试")
            # 1秒后重试验证
            QTimer.singleShot(1000, lambda: self._on_page_loaded(True))

    def generate_threejs_page(self):
        """生成Three.js渲染页面，确保全局对象正确初始化"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Three.js GLB Viewer</title>
            <!-- 使用ES Modules方式加载Three.js -->
            <script type="importmap">
                {
                    "imports": {
                        "three": "./runtime/3js/build/three.module.min.js",
                        "three/addons/": "./runtime/3js/examples/jsm/"
                    }
                }
            </script>
            <style>
                body { margin: 0; overflow: hidden; height: 100vh; }
                #loading { 
                    position: absolute; top: 50%; left: 50%; 
                    transform: translate(-50%, -50%); color: white;
                    font-family: Arial; background: rgba(0,0,0,0.5); padding: 10px;
                    z-index: 100;
                }
            </style>
        </head>
        <body>
            <div id="loading">初始化渲染环境...</div>
            
            <!-- 确保全局命名空间在模块加载前定义 -->
            <script>
                // 优先创建全局对象，避免模块加载时无法访问
                window.threeViewer = {
                    loadGLB: function() { console.error("尚未初始化"); },
                    setLightIntensity: function() { console.error("尚未初始化"); },
                    setAmbientIntensity: function() { console.error("尚未初始化"); }
                };
            </script>
            
            <!-- 模块脚本 -->
            <script type="module">
                import * as THREE from 'three';
                import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
                import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
                
                // 初始化场景
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x1a1a1a);
                
                // 相机和渲染器
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({ antialias: true });
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);
                
                // 灯光设置
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
                scene.add(ambientLight);
                
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(3, 3, 3);
                scene.add(directionalLight);
                
                // 控制器
                const controls = new OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                
                // 模型变量
                let model = null;
                
                // 窗口大小调整
                function onWindowResize() {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }
                window.addEventListener('resize', onWindowResize);
                
                // 渲染循环
                function animate() {
                    requestAnimationFrame(animate);
                    controls.update();
                    renderer.render(scene, camera);
                }
                animate();
                
                // 定义加载函数
                function loadGLB(base64Data) {
                    if (model) {
                        scene.remove(model);
                        model = null;
                    }
                    
                    try {
                        const binaryString = atob(base64Data);
                        const bytes = new Uint8Array(binaryString.length);
                        for (let i = 0; i < binaryString.length; i++) {
                            bytes[i] = binaryString.charCodeAt(i);
                        }
                        
                        const loader = new GLTFLoader();
                        loader.parse(
                            bytes.buffer, '',
                            (gltf) => {
                                model = gltf.scene;
                                scene.add(model);
                                
                                // 自动调整模型大小和位置
                                const box = new THREE.Box3().setFromObject(model);
                                const size = box.getSize(new THREE.Vector3()).length();
                                const center = box.getCenter(new THREE.Vector3());
                                
                                const modelScale = 5 / size;
                                model.position.x = -center.x * modelScale;
                                model.position.y = -center.y * modelScale;
                                model.position.z = -center.z * modelScale;
                                model.scale.set(modelScale, modelScale, modelScale);
                                
                                camera.position.z = size * 1.5;
                                document.getElementById('loading').style.display = 'none';
                            },
                            (xhr) => {
                                const percent = (xhr.loaded / xhr.total * 100).toFixed(0);
                                document.getElementById('loading').textContent = `加载中: ${percent}%`;
                            },
                            (error) => {
                                console.error('模型加载错误:', error);
                                document.getElementById('loading').textContent = '加载失败: ' + error.message;
                            }
                        );
                    } catch (error) {
                        console.error('数据处理错误:', error);
                        document.getElementById('loading').textContent = '数据处理失败';
                    }
                }
                
                // 定义光源控制函数
                function setLightIntensity(intensity) {
                    directionalLight.intensity = intensity;
                }
                
                function setAmbientIntensity(intensity) {
                    ambientLight.intensity = intensity;
                }
                
                // 确保全局对象被正确赋值，使用立即执行函数确保执行顺序
                (function() {
                    // 覆盖全局对象的方法
                    window.threeViewer.loadGLB = loadGLB;
                    window.threeViewer.setLightIntensity = setLightIntensity;
                    window.threeViewer.setAmbientIntensity = setAmbientIntensity;
                    // 通知初始化完成
                    document.getElementById('loading').textContent = '渲染环境就绪，请加载模型';
                })();
            </script>
        </body>
        </html>
        """

    # 对外控制接口 - 确保调用时环境已初始化
    def load_glb_data(self, base64_data):
        """加载Base64编码的GLB数据，带初始化检查"""
        if not self.initialized:
            print("Three.js环境尚未准备好，将在1秒后重试")
            QTimer.singleShot(1000, lambda: self.load_glb_data(base64_data))
            return

        # 转义可能的特殊字符
        escaped_data = base64_data.replace("'", "\\'").replace('"', '\\"')
        self.page.runJavaScript(f"window.threeViewer.loadGLB('{escaped_data}');")

    def set_light_intensity(self, intensity):
        """设置光源强度，带初始化检查"""
        if not self.initialized:
            QTimer.singleShot(1000, lambda: self.set_light_intensity(intensity))
            return
        self.page.runJavaScript(
            f"window.threeViewer.setLightIntensity({intensity / 100.0});"
        )

    def set_ambient_intensity(self, intensity):
        """设置环境光强度，带初始化检查"""
        if not self.initialized:
            QTimer.singleShot(1000, lambda: self.set_ambient_intensity(intensity))
            return
        self.page.runJavaScript(
            f"window.threeViewer.setAmbientIntensity({intensity / 100.0});"
        )


class CustomWebEnginePage(QWebEnginePage):
    """自定义Web页面，处理链接点击和错误"""

    def __init__(self, parent=None):
        super().__init__(parent)

    # 重写javaScriptConsoleMessage方法来捕获JS错误
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """捕获并显示JavaScript错误"""
        print(f"JS错误: {message} (行号: {line_number})")

    def acceptNavigationRequest(self, url, _type, is_main_frame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)
            return False
        return super().acceptNavigationRequest(url, _type, is_main_frame)


class GLBLoaderThread(QThread):
    """异步加载模型的线程"""

    load_finished = Signal(bool, str, bytes)
    progress_updated = Signal(int)

    def __init__(self, url=None, file_path=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.file_path = file_path

    def run(self):
        try:
            file_data = None
            if self.url:
                self.progress_updated.emit(0)
                response = requests.get(self.url, stream=True, verify=False)
                total_size = int(response.headers.get("content-length", 0))
                downloaded_size = 0
                file_data = b""

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file_data += chunk
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            self.progress_updated.emit(
                                int((downloaded_size / total_size) * 100)
                            )

                if response.status_code != 200:
                    self.load_finished.emit(
                        False, f"下载失败: {response.status_code}", None
                    )
                    return

            elif self.file_path:
                if not os.path.exists(self.file_path):
                    self.load_finished.emit(False, "文件不存在", None)
                    return

                with open(self.file_path, "rb") as f:
                    file_data = f.read()
                self.progress_updated.emit(100)

            else:
                self.load_finished.emit(False, "未指定加载源", None)
                return

            self.load_finished.emit(True, "加载成功", file_data)

        except Exception as e:
            self.load_finished.emit(False, f"加载失败: {str(e)}", None)


class GLBViewerWidget(QWidget):
    """GLB模型查看器控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.loader_thread = None

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.status_label = QLabel("请加载GLB模型")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        main_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        content_layout = QHBoxLayout()

        self.gl_window = ThreeJSViewerWindow()
        content_layout.addWidget(self.gl_window, 4)

        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        control_layout.addWidget(
            QLabel("Light Source Brightness")
        )  # QLabel("光源强度"))
        self.light_slider = QSlider(Qt.Horizontal)
        self.light_slider.setRange(0, 100)
        self.light_slider.setValue(80)
        control_layout.addWidget(self.light_slider)

        control_layout.addWidget(
            QLabel("Environmental Light Brightness")
        )  # ("环境光强度"))
        self.ambient_slider = QSlider(Qt.Horizontal)
        self.ambient_slider.setRange(0, 100)
        self.ambient_slider.setValue(30)
        control_layout.addWidget(self.ambient_slider)

        info_label = QLabel(
            "Tips: Press mouse left button to turn the model, \nspinwheel to scale,\nright button to move"
        )  # ("提示: 按住鼠标左键拖动可旋转模型\n滚轮缩放，右键平移")
        info_label.setStyleSheet("margin-top: 20px; color: #666; font-size: 12px;")
        control_layout.addWidget(info_label)

        control_layout.addStretch()
        content_layout.addWidget(control_panel, 1)

        main_layout.addLayout(content_layout, 1)

        self.light_slider.valueChanged.connect(self.gl_window.set_light_intensity)
        self.ambient_slider.valueChanged.connect(self.gl_window.set_ambient_intensity)

    def load_from_file(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择GLB文件", "", "GLB Files (*.glb)"
            )
            if not file_path:
                return

        self.status_label.setText(
            f"Loading: {os.path.basename(file_path)}"
        )  # (f"正在加载: {os.path.basename(file_path)}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.terminate()

        self.loader_thread = GLBLoaderThread(file_path=file_path)
        self.loader_thread.progress_updated.connect(self.progress_bar.setValue)
        self.loader_thread.load_finished.connect(self._on_load_finished)
        self.loader_thread.start()

    def load_from_url(self, url):
        self.status_label.setText(
            f"Loading: {url.split('/')[-1]}"
        )  # (f"正在下载: {url.split('/')[-1]}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.terminate()

        self.loader_thread = GLBLoaderThread(url=url)
        self.loader_thread.progress_updated.connect(self.progress_bar.setValue)
        self.loader_thread.load_finished.connect(self._on_load_finished)
        self.loader_thread.start()

    def _on_load_finished(self, success, message, file_data):
        if success and file_data:
            self.status_label.setText("Parsing model...")  # ("正在解析模型...")
            try:
                base64_data = base64.b64encode(file_data).decode("utf-8")
                self.gl_window.load_glb_data(base64_data)
                self.status_label.setText("Finished loading model")  # ("模型加载完成")
            except Exception as e:
                self.status_label.setText(
                    f"Load failed:{str(e)}"
                )  # (f"解析失败: {str(e)}")
        else:
            self.status_label.setText(
                f"Load failed:{message}"
            )  # (f"加载失败: {message}")

        self.progress_bar.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("Three.js GLB模型查看器")
    main_window.resize(1000, 700)

    layout = QVBoxLayout(main_window)
    glb_viewer = GLBViewerWidget()
    layout.addWidget(glb_viewer)

    main_window.show()
    # 延迟加载模型，确保页面有足够时间初始化
    QTimer.singleShot(
        2000, lambda: glb_viewer.load_from_url("http://localhost/Box.glb")
    )

    sys.exit(app.exec())
