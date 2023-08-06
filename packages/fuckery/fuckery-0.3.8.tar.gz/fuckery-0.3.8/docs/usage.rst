=====
Usage
=====

To use pyFuckery in a project simply import the package, instantiate a VM and execute your brainfuck program::

	import fuckery
	vm = fuckery.vm.VirtualMachine()
	program = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
	vm.parse_and_run(program)

You can also swap out the input / output streams used by the VM, if stdin / stderr are not appropriate for your application::

	import fuckery
	import io
	outstream = io.StringIO()
	vm = fuckery.vm.VirtualMachine()
	vm.stream_out = outstream
	program = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
	vm.parse_and_run(program)
	vm.out_stream.seek(0)
	print(vm.out_stream.read())

