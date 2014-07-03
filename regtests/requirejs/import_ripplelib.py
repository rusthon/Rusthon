'''test ripple library'''
# sudo npm install -g ripple-lib
# https://github.com/ripple/ripple-lib/blob/develop/docs/GUIDES.md

import ripple-lib as ripple

def main():
	R = new(ripple.Remote(
		trusted=True, 
		local_signing=True,
		local_fee=True,
		fee_cushion=1.5,
		servers = [
			{'host':'s1.ripple.com', 'port':443, 'secure':True}
		]
	))
	def on_connect():
		print('connected!')
		test2(R)

	R.connect( on_connect )

def test2(R):
	req = R.request_server_info()
	def on_server_info_ok(r):
		print('info ok')
		print(r)
	def on_server_info_err(e):
		print('info err')
		print(e)

	req.on('success', on_server_info_ok)
	req.on('error', on_server_info_err)

	req.request()

	print('ripple-lib test complete')
