from ..models import Order, OrderItem
import uuid
from .book_service import BookService

class CartService:
  @staticmethod
  def get_cart_for_user(user):
    if not user.is_authenticated:
      return { 'order': None, 'items': [] }
    
    order, _ = Order.objects.get_or_create(customer=user, complete=False)
    items = order.orderitem_set.all()
    return { 'order': order, 'items': items }
  
  @staticmethod
  def get_items_count(user):
    if not user.is_authenticated:
      return 0
    
    order, _ = Order.objects.get_or_create(customer=user, complete=False)
    return order.orderitem_set.count()
  
  @staticmethod
  def checkout(order, shipping_address):
    shipping_address.save()
    order.complete = True
    order.transaction_id = str(uuid.uuid4())
    order.save()

  @staticmethod
  def edit_cart(user, edit_cart_request):
    book_id = edit_cart_request['bookId']
    quantity = edit_cart_request['quantity']

    order, _ = Order.objects.get_or_create(customer=user, complete=False)
    book = BookService.find_by_id(book_id)
    book_order_item, _ = OrderItem.objects.get_or_create(book=book, order=order)
    new_quantity = book_order_item.quantity + quantity
    is_item_removed = ('removeItem' in edit_cart_request and edit_cart_request['removeItem']) or new_quantity <= 0

    if is_item_removed:
      book_order_item.delete()
    else:
      book_order_item.quantity = new_quantity
      book_order_item.save()

  @staticmethod
  def set_cart_quantity(user, set_cart_request):
    book_id = set_cart_request['bookId']
    new_quantity = set_cart_request['newQuantity']
    order, _ = Order.objects.get_or_create(customer=user, complete=False)
    book = BookService.find_by_id(book_id)
    book_order_item, _ = OrderItem.objects.get_or_create(book=book, order=order)
    book_order_item.quantity = new_quantity
    book_order_item.save()
    
    

    