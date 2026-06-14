"""数据处理工具"""
import json
import yaml
import pandas as pd
from pathlib import Path


class DataHandler:
    """数据处理类"""
    
    @staticmethod
    def load_json(file_path):
        """加载JSON文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            JSON数据
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_yaml(file_path):
        """加载YAML文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            YAML数据
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_excel(file_path, sheet_name=0):
        """加载Excel文件
        
        Args:
            file_path: 文件路径
            sheet_name: 工作表名称或索引
        
        Returns:
            DataFrame对象
        """
        return pd.read_excel(file_path, sheet_name=sheet_name)
    
    @staticmethod
    def load_csv(file_path):
        """加载CSV文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            DataFrame对象
        """
        return pd.read_csv(file_path)
    
    @staticmethod
    def save_json(data, file_path):
        """保存为JSON文件
        
        Args:
            data: 数据
            file_path: 文件路径
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def save_yaml(data, file_path):
        """保存为YAML文件
        
        Args:
            data: 数据
            file_path: 文件路径
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
