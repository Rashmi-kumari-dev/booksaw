from ..models import Book

class BookService:
  @staticmethod
  def find_all():
    return Book.objects.all()
  
  @staticmethod
  def find_by_id(id):
    return Book.objects.get(id=id)
  
  @staticmethod
  def find_all_featured():
    return Book.objects.filter(is_featured=True)
  
  @staticmethod
  def find_all_discounted():
    return Book.objects.filter(discount__gt=0)
  
  @staticmethod
  def find_all_genre_groups():
    return {
      'romance': BookService.__find_all_by_genre('Romance'),
      'technology': BookService.__find_all_by_genre('Technology'),
      'fantasy': BookService.__find_all_by_genre('Fantasy'),
      'adventure': BookService.__find_all_by_genre('Adventure'),
      'non_fiction': BookService.__find_all_by_genre('Non-fiction'),
    }

  @staticmethod
  def find_all_covers():
    return Book.objects.all()[:5]
  
  @staticmethod
  def find_best_selling():
    return Book.objects.last()

  @staticmethod
  def __find_all_by_genre(genre):
    return Book.objects.filter(genre__icontains=genre)
  
