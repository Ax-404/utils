import logging
from typing import List, Callable, Optional, Dict, Any
from contextlib import contextmanager
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TransactionError(Exception):
    """Exception raised for transaction-related errors"""
    pass

class TransactionManager:
    """Gère les transactions et le rollback en cas d'échec
    
    Cette classe permet de gérer les transactions de manière atomique,
    avec la possibilité de faire un rollback en cas d'erreur.
    
    Attributes:
        transaction_stack (List[List[Callable]]): Pile des transactions en cours
        rollback_actions (List[Callable]): Actions de rollback pour la transaction courante
        transaction_log (List[Dict]): Journal des transactions
    """
    
    def __init__(self):
        self.transaction_stack: List[List[Callable]] = []
        self.rollback_actions: List[Callable] = []
        self.transaction_log: List[Dict[str, Any]] = []
    
    def begin_transaction(self) -> None:
        """Démarre une nouvelle transaction"""
        self.transaction_stack.append([])
        self.transaction_log.append({
            'start_time': datetime.now(),
            'actions': [],
            'status': 'in_progress'
        })
        logger.info("Transaction started")
    
    def add_rollback_action(self, action: Callable) -> None:
        """Ajoute une action de rollback à la transaction courante
        
        Args:
            action (Callable): Fonction à exécuter en cas de rollback
        """
        if self.transaction_stack:
            self.transaction_stack[-1].append(action)
            self.transaction_log[-1]['actions'].append({
                'type': 'rollback_action',
                'timestamp': datetime.now()
            })
    
    def add_action(self, action_type: str, details: Dict[str, Any]) -> None:
        """Ajoute une action au journal de la transaction courante
        
        Args:
            action_type (str): Type d'action (create, update, delete, etc.)
            details (Dict[str, Any]): Détails de l'action
        """
        if self.transaction_log:
            self.transaction_log[-1]['actions'].append({
                'type': action_type,
                'details': details,
                'timestamp': datetime.now()
            })
    
    def commit(self) -> None:
        """Valide la transaction courante"""
        if self.transaction_stack:
            self.transaction_stack.pop()
            if self.transaction_log:
                self.transaction_log[-1]['status'] = 'committed'
                self.transaction_log[-1]['end_time'] = datetime.now()
            logger.info("Transaction committed")
    
    def rollback(self) -> None:
        """Annule la transaction courante"""
        if self.transaction_stack:
            actions = self.transaction_stack.pop()
            if self.transaction_log:
                self.transaction_log[-1]['status'] = 'rolled_back'
                self.transaction_log[-1]['end_time'] = datetime.now()
            
            for action in reversed(actions):
                try:
                    action()
                except Exception as e:
                    logger.error(f"Error during rollback: {str(e)}")
                    raise TransactionError(f"Rollback failed: {str(e)}")
            
            logger.info("Transaction rolled back")
    
    def get_transaction_log(self) -> List[Dict[str, Any]]:
        """Récupère le journal des transactions
        
        Returns:
            List[Dict[str, Any]]: Journal des transactions
        """
        return self.transaction_log
    
    @contextmanager
    def transaction(self):
        """Contexte de transaction pour une utilisation avec 'with'
        
        Example:
            with transaction_manager.transaction():
                # Code à exécuter dans la transaction
                pass
        """
        self.begin_transaction()
        try:
            yield
            self.commit()
        except Exception as e:
            self.rollback()
            raise TransactionError(f"Transaction failed: {str(e)}")
    
    def clear_logs(self, older_than_days: int = 30) -> None:
        """Nettoie les anciens logs de transaction
        
        Args:
            older_than_days (int): Nombre de jours après lequel les logs sont supprimés
        """
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        self.transaction_log = [
            log for log in self.transaction_log
            if log['start_time'] > cutoff_date
        ] 