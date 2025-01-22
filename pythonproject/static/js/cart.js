//主要處理購物車頁面中，點擊按紐以更新(新增或取消)商品數量的行為
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		//若使用者未登入，則將資料儲存至資料庫中
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
		//若使用者已登入則更新資料
			updateUserOrder(productId, action)
		}
	})
}

// 當使用者未登入時，將商品更新到 Cookie
function addCookieItem(productId, action){
	console.log('Not logged in...')

	//增加按紐：當點選"加入"時，購物車商品數量會加1
	if(action == 'add'){
		if(cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}
		else{
			cart[productId]['quantity'] += 1
		}
	}

	//減少按紐：當點選"移除"時，購物車商品數量會減1
	if(action == 'remove'){
		cart[productId]['quantity'] -= 1

		//商品數量小與0則會直接移除商品
		if(cart[productId]['quantity'] <= 0){
			console.log('Remove Item')
			delete cart[productId]
		}
	}

	//更新並儲存購物車資料至Cookie
	console.log('Cart:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
	location.reload()

}

// 當使用者已登入時，則直接更新資料
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/store/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) =>{
		   return response.json()
		})
		.then((data) =>{
		   console.log('data:',data)
           location.reload()
		})
}