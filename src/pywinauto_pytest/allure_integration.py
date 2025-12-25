import os
import time
from typing import Optional, Any
from pywinauto import Application
from .logger import logger


class AllureIntegration:
    """Allure 报告集成"""
    
    def __init__(self):
        self._step_count = 0
    
    def start_step(self, name: str, description: Optional[str] = None) -> None:
        """开始一个测试步骤"""
        try:
            import allure
            with allure.step(name):
                if description:
                    allure.attach(description, name="描述")
        except ImportError:
            logger.warning("allure 模块未安装，无法生成 Allure 报告")
    
    def stop_step(self) -> None:
        """停止当前测试步骤"""
        # Allure 步骤通过上下文管理器自动管理，不需要手动停止
        pass
    
    def attach_screenshot(self, name: str = "截图") -> None:
        """添加截图到 Allure 报告"""
        try:
            import allure
            from PIL import ImageGrab
            
            # 截取当前屏幕
            screenshot = ImageGrab.grab()
            
            # 保存截图到临时文件
            screenshot_path = f"screenshot_{int(time.time())}.png"
            screenshot.save(screenshot_path)
            
            # 附加截图到 Allure 报告
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.PNG)
            
            # 删除临时文件
            os.remove(screenshot_path)
            logger.info(f"已添加截图到 Allure 报告: {name}")
        except ImportError as e:
            logger.warning(f"无法添加截图到 Allure 报告: {str(e)}")
        except Exception as e:
            logger.error(f"添加截图到 Allure 报告失败: {str(e)}")
    
    def attach_file(self, file_path: str, name: str, file_type: str = "txt") -> None:
        """添加文件到 Allure 报告"""
        try:
            import allure
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.warning(f"文件不存在，无法添加到 Allure 报告: {file_path}")
                return
            
            # 确定文件类型
            attachment_type = self._get_attachment_type(file_type)
            
            # 附加文件到 Allure 报告
            with open(file_path, "rb") as f:
                allure.attach(f.read(), name=name, attachment_type=attachment_type)
            
            logger.info(f"已添加文件到 Allure 报告: {name}")
        except ImportError as e:
            logger.warning(f"无法添加文件到 Allure 报告: {str(e)}")
        except Exception as e:
            logger.error(f"添加文件到 Allure 报告失败: {str(e)}")
    
    def add_tag(self, tag: str) -> None:
        """添加标签到 Allure 报告"""
        try:
            import allure
            allure.dynamic.tag(tag)
        except ImportError:
            logger.warning("allure 模块未安装，无法添加标签到 Allure 报告")
    
    def add_description(self, description: str) -> None:
        """添加描述到 Allure 报告"""
        try:
            import allure
            allure.dynamic.description(description)
        except ImportError:
            logger.warning("allure 模块未安装，无法添加描述到 Allure 报告")
    
    def add_link(self, url: str, name: str, link_type: str = "link") -> None:
        """添加链接到 Allure 报告"""
        try:
            import allure
            allure.dynamic.link(url, name=name, link_type=link_type)
        except ImportError:
            logger.warning("allure 模块未安装，无法添加链接到 Allure 报告")
    
    def _get_attachment_type(self, file_type: str) -> Any:
        """根据文件类型获取 Allure 附件类型"""
        import allure
        
        type_map = {
            "txt": allure.attachment_type.TEXT,
            "json": allure.attachment_type.JSON,
            "xml": allure.attachment_type.XML,
            "html": allure.attachment_type.HTML,
            "png": allure.attachment_type.PNG,
            "jpg": allure.attachment_type.JPG,
            "jpeg": allure.attachment_type.JPG,
            "gif": allure.attachment_type.GIF,
            "pdf": allure.attachment_type.PDF,
        }
        
        return type_map.get(file_type.lower(), allure.attachment_type.TEXT)
