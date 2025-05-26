import pandas as pd
import logging
from contextlib import contextmanager
from typing import Optional, Any, Dict, List

logger = logging.getLogger(__name__)


#from previous project
class DataFrameManager:
    """Utility class for safe DataFrame handling with automatic memory management"""
    
    @staticmethod
    @contextmanager
    def safe_dataframe(data: List[Dict[str, Any]] = None, df: Optional[pd.DataFrame] = None):
        """
        Context manager for safe DataFrame handling with automatic cleanup
        
        Args:
            data: List of dictionaries to create DataFrame from
            df: Existing DataFrame to manage
            
        Yields:
            pd.DataFrame: The managed DataFrame
        """
        try:
            if data is not None:
                df = pd.DataFrame(data)
            elif df is None:
                raise ValueError("Either data or df must be provided")
                
            yield df
            
        except Exception as e:
            logger.error(f"Error handling DataFrame: {str(e)}")
            raise
        finally:
            if df is not None:
                try:
                    # Clear DataFrame memory
                    df = None
                    # Force garbage collection
                    import gc
                    gc.collect()
                except Exception as e:
                    logger.warning(f"Error cleaning up DataFrame: {str(e)}")
    
    @staticmethod
    def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame memory usage
        
        Args:
            df: DataFrame to optimize
            
        Returns:
            pd.DataFrame: Optimized DataFrame
        """
        try:
            # Make a copy to avoid modifying the original
            df_optimized = df.copy()
            
            # Optimize numeric columns
            for col in df_optimized.select_dtypes(include=['int']).columns:
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
            
            for col in df_optimized.select_dtypes(include=['float']).columns:
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
            
            # Optimize categorical columns
            for col in df_optimized.select_dtypes(include=['object']).columns:
                if df_optimized[col].nunique() / len(df_optimized) < 0.5:  # If less than 50% unique values
                    df_optimized[col] = df_optimized[col].astype('category')
            
            return df_optimized
            
        except Exception as e:
            logger.error(f"Error optimizing DataFrame memory: {str(e)}")
            return df  # Return original DataFrame if optimization fails 