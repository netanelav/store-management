from abc import ABC, abstractmethod


class BaseDatabaseAdapter(ABC):
    # Create
    @abstractmethod
    def add_category(self):
        pass

    @abstractmethod
    def add_or_edit_product(self):
        pass

    # Read
    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def get_product(self, id):
        pass

    @abstractmethod
    def products_by_category(self, id):
        pass

    # Delete
    @abstractmethod
    def delete_category(self, id):
        pass

    @abstractmethod
    def delete_product(self, id):
        pass
