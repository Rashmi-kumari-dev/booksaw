from ..models import Order, OrderItem

class OrderService:
  @staticmethod
  def get_order_history_for_user(user):
    return Order.objects.filter(customer=user, complete=True).order_by("-id")
  
  @staticmethod
  def find_by_id(id):
    return Order.objects.get(id=id)
  
  @staticmethod
  def find_all_items(order):
    return order.orderitem_set.all()