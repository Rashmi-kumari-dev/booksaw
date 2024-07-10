const cart = {
  editCart: function(bookId, quantity, { bookName, removeItem, message } = { bookName: '', removeItem: false, message: null }) {
    $.ajax({
      url: "/editCart/",
      method: 'POST',
      data: JSON.stringify({ bookId, quantity, removeItem }),
      contentType: "application/json; charset=utf-8",
    }).done(function(d) {
      if(message) {
        showToast(message);
      }
      cart.setCartItemQuantity(d.cartItemCount)
    });
  },
  setCartQuantity: function(bookId, newQuantity, bookPrice) {
    $.ajax({
      url: "/setCartQuantity/",
      method: 'POST',
      data: JSON.stringify({ bookId, newQuantity }),
      contentType: "application/json; charset=utf-8",
    }).done(function(d) {
      const spanText = document.getElementById(`cart-item-book-id-${bookId}`)
      spanText.innerHTML = `$ ${bookPrice * newQuantity}.00`
      cart.setCartItemQuantity(d.cartItemCount)
    });
  },
  /**
   * 
   * @param {Event} event 
   */
  onEditCartQuantity: function(inputEle) {
    const bookId = inputEle.getAttribute('data-book-id');
    const bookPrice = inputEle.getAttribute('data-book-price')
    cart.setCartQuantity(bookId, parseInt(inputEle.value), bookPrice);
  },
  setCartItemQuantity: function(cartItemQuantity) {
    const cartItemCountEle = document.getElementById('cart-item-count')
    cartItemCountEle.innerHTML = `Cart (${cartItemQuantity})`
  }
}

 