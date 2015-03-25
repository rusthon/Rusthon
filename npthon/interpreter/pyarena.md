pyarena.c
-----------


@pyarena.c
```c
#include "Python.h"
#include "pyarena.h"
```

Measurements with standard library modules suggest the average
allocation is about 20 bytes and that most compiles use a single
block.
TODO(jhylton): Think about a realloc API, maybe just for the last
allocation?

```c
#define DEFAULT_BLOCK_SIZE 8192
#define ALIGNMENT               8
#define ALIGNMENT_MASK          (ALIGNMENT - 1)
#define ROUNDUP(x)              (((x) + ALIGNMENT_MASK) & ~ALIGNMENT_MASK)
typedef struct _block {
```

 Read-only after initialization.  The first such byte starts at
 ab_mem.

```c
    size_t ab_size;
```

 to pass out starts at ab_mem + ab_offset.

```c
    size_t ab_offset;
```

 all blocks owned by the arena.  These are linked via the
 ab_next member.

```c
    struct _block *ab_next;
```

 only after initialization.

```c
    void *ab_mem;
} block;
```

and a list of PyObject* pointers.  PyObjects are decrefed
when the arena is freed.

```c
struct _arena {
```

It is used only to find the first block when the arena is
being freed.

```c
    block *a_head;
```

ab_next field should be NULL.  If it is not-null after a
call to block_alloc(), it means a new block has been allocated
and a_cur should be reset to point it.

```c
    block *a_cur;
```

pointers associated with this area.  They will be DECREFed
when the arena is freed.

```c
    PyObject *a_objects;
#if defined(Py_DEBUG)
```

Debug output

```c
    size_t total_allocs;
    size_t total_size;
    size_t total_blocks;
    size_t total_block_size;
    size_t total_big_blocks;
#endif
};
static block *
block_new(size_t size)
{
```

>ab_mem points just past header.

```c
    block *b = (block *)malloc(sizeof(block) + size);
    if (!b)
        return NULL;
    b->ab_size = size;
    b->ab_mem = (void *)(b + 1);
    b->ab_next = NULL;
    b->ab_offset = ROUNDUP((Py_uintptr_t)(b->ab_mem)) -
      (Py_uintptr_t)(b->ab_mem);
    return b;
}
static void
block_free(block *b) {
    while (b) {
        block *next = b->ab_next;
        free(b);
        b = next;
    }
}
static void *
block_alloc(block *b, size_t size)
{
    void *p;
    assert(b);
    size = ROUNDUP(size);
    if (b->ab_offset + size > b->ab_size) {
```

the default block, allocate a one-off block that is
>exactly the right size.

```c
```

TODO(jhylton): Think about space waste at end of block

```c
        block *newbl = block_new(
                        size < DEFAULT_BLOCK_SIZE ?
                        DEFAULT_BLOCK_SIZE : size);
        if (!newbl)
            return NULL;
        assert(!b->ab_next);
        b->ab_next = newbl;
        b = newbl;
    }
    assert(b->ab_offset + size <= b->ab_size);
    p = (void *)(((char *)b->ab_mem) + b->ab_offset);
    b->ab_offset += size;
    return p;
}
PyArena *
PyArena_New()
{
    PyArena* arena = (PyArena *)malloc(sizeof(PyArena));
    if (!arena)
        return (PyArena*)PyErr_NoMemory();
    arena->a_head = block_new(DEFAULT_BLOCK_SIZE);
    arena->a_cur = arena->a_head;
    if (!arena->a_head) {
        free((void *)arena);
        return (PyArena*)PyErr_NoMemory();
    }
    arena->a_objects = PyList_New(0);
    if (!arena->a_objects) {
        block_free(arena->a_head);
        free((void *)arena);
        return (PyArena*)PyErr_NoMemory();
    }
#if defined(Py_DEBUG)
    arena->total_allocs = 0;
    arena->total_size = 0;
    arena->total_blocks = 1;
    arena->total_block_size = DEFAULT_BLOCK_SIZE;
    arena->total_big_blocks = 0;
#endif
    return arena;
}
void
PyArena_Free(PyArena *arena)
{
    assert(arena);
#if defined(Py_DEBUG)
```

fprintf(stderr,
"alloc=%d size=%d blocks=%d block_size=%d big=%d objects=%d\n",
arena->total_allocs, arena->total_size, arena->total_blocks,
arena->total_block_size, arena->total_big_blocks,
PyList_Size(arena->a_objects));

```c
#endif
    block_free(arena->a_head);
```

is sys.getobjects(0), in which case there will be two references.
assert(arena->a_objects->ob_refcnt == 1);

```c
    Py_DECREF(arena->a_objects);
    free(arena);
}
void *
PyArena_Malloc(PyArena *arena, size_t size)
{
    void *p = block_alloc(arena->a_cur, size);
    if (!p)
        return PyErr_NoMemory();
#if defined(Py_DEBUG)
    arena->total_allocs++;
    arena->total_size += size;
#endif
```

Reset cur if we allocated a new block.

```c
    if (arena->a_cur->ab_next) {
        arena->a_cur = arena->a_cur->ab_next;
#if defined(Py_DEBUG)
        arena->total_blocks++;
        arena->total_block_size += arena->a_cur->ab_size;
        if (arena->a_cur->ab_size > DEFAULT_BLOCK_SIZE)
            ++arena->total_big_blocks;
#endif
    }
    return p;
}
int
PyArena_AddPyObject(PyArena *arena, PyObject *obj)
{
    int r = PyList_Append(arena->a_objects, obj);
    if (r >= 0) {
        Py_DECREF(obj);
    }
    return r;
}
```
___