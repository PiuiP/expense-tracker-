from decimal import Decimal
from uuid import UUID

from app.models.transaction import TransactionCreate, TransactionResponse
from app.repositories.transaction import ITransactionRepository
from app.repositories.category import ICategoryRepository

class TransactionService():
    def __init__(self, repository: ITransactionRepository, repository_cat: ICategoryRepository):
        self.repository = repository
        self.repository_cat = repository_cat

    async def create_transaction(self, data: TransactionCreate, category_ids: list[UUID]) -> TransactionResponse:
        transaction = await self.repository.create(data)
        await self.repository.add_categories(transaction.id, category_ids)
        return transaction

    async def get_transaction_by_id(self, transaction_id: UUID) -> TransactionResponse:
        return await self.repository.get_by_id(transaction_id)

    async def get_all_transactions(self) -> list[TransactionResponse]:
        return await self.repository.get_all()

    async def update_transaction(self, transaction_id: UUID, new_data: dict) -> TransactionResponse:
        old_transaction = await self.repository.get_by_id(transaction_id)

        old_dict = old_transaction.model_dump()

        old_dict.update(new_data)
        old_dict.pop('id', None) #лишнее
        old_dict.pop('created_at', None) #лишнее

        new_transaction = TransactionCreate(**old_dict)

        return await self.repository.update(transaction_id, new_transaction)

    async def delete_transaction(self, transaction_id: UUID) -> bool:
        return await self.repository.delete(transaction_id)

    async def get_filtered_transactions(self, category_id, date_from, date_to):
        if not date_from or not date_to:
            raise ValueError("Даты date_from и date_to обязательны")
            
        #category_id не передан -> ищем по всем категориям
        transactions = await self.repository.get_filtered(category_id, date_from, date_to)

        return list(transactions)

#TODO: в абстрактный класс репозитория добавить метод, который будет на sql сортировать по типу операции
#тогда этот сервис будет просто вызывать метод репозитория и возвращать результат -> rout-> client
    async def get_transaction_stats(self) -> dict:
        transaction = await self.repository.get_all()

        total_income = Decimal('0.0')
        total_expense = Decimal('0.0')

        for t in transaction:
            amount = Decimal(str(t.amount)) if not isinstance(t.amount, Decimal) else t.amount
            if t.type_of_transaction == 'income':
                total_income += amount
            elif t.type_of_transaction == 'expense':
                total_expense += amount
 #standart json cannot serialize Decimal object -> convert to string
        return{
            "total_income": str(total_income),
            "total_expense": str(total_expense),
            "balance": str(total_income - total_expense)
        }    
#TODO: the same like previous
    async def get_expenses_by_category(self) -> dict:
            transaction = await self.repository.get_all()
            categories = await self.repository_cat.get_all()

            cat_map = {cat.id: cat.name for cat in categories} #ID категории -> название категории
            expenses = {name: Decimal('0.0') for name in cat_map.values()}

            for t in transaction:
                if t.type_of_transaction == 'expense':
                    cat_ids = await self.repository.get_categories_by_transaction_id(t.id)
                    amount = Decimal(str(t.amount)) if not isinstance(t.amount, Decimal) else t.amount
                    
                    for c in cat_ids:
                        cat_name = cat_map.get(c, "NO CATEGORY")
                        if cat_name not in expenses:
                            expenses[cat_name] = Decimal('0.0')
                        expenses[cat_name] += amount

            return {name: str(amount) for name, amount in expenses.items()}