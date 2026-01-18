class DocumentStorageService:
    """
    Interfaz lógica de almacenamiento.
    """

    def save(self, document):
        raise NotImplementedError

    def get(self, document_id):
        raise NotImplementedError

    def delete(self, document):
        raise NotImplementedError


class DatabaseStorageService(DocumentStorageService):
    """
    Implementación V1: Base de datos.
    """

    def save(self, document):
        document.storage_type = "DB"
        document.save()

    def get(self, document_id):
        from .models import Document
        return Document.objects.get(id=document_id)

    def delete(self, document):
        document.delete()
