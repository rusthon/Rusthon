
class _fake_sys:
	def __init__(self):
		self.stdin = process.stdin
		self.stdout = process.stdout
		self.stderr = process.stderr
		self.argv = process.argv

	def exit(self):
		process.exit()

sys = _fake_sys()
