#include<pthread.h>
#include<string>
#include<vector>


class DataObject;
class HeapObj;

enum ObjectType {LONG, DOUBLE, STRING, ARRAY, ALL, NONE};

class DataObject {
    public:
        union {
            long v_long;
            double v_double;
            const std::string * v_string;
        };

        HeapObj * v_array;
        long heap_offset;

        ObjectType type;

        DataObject(ObjectType new_type);
        DataObject(HeapObj * arr);
        DataObject(const DataObject& copy);
        ~DataObject();
        DataObject * set_type(ObjectType new_type);
        DataObject * padd(long increment);

        long get_long() const;
        long get_size(bool destr, DataObject ** vm) const;
        double get_double() const;
        const std::string * get_string() const;

        inline DataObject * retrieve(long offset, DataObject ** vm);
        HeapObj * get_heap_obj(DataObject ** vm);

        void print();
        inline void safe_print() const;
};

class HeapObj {
    private:
        DataObject ** array;
        unsigned int capacity;

        bool do_destroy;
        bool destructed;

    public:
        unsigned int orig_size;
        ObjectType cast_type;
        std::vector<HeapObj *> * concats;
        std::vector<DataObject *> * incats;
        long refcount;
        unsigned int ccount;

        HeapObj(unsigned int size, int refcnt);
        HeapObj(unsigned int offset, DataObject ** vm);
        HeapObj(const HeapObj& copy);
        HeapObj(HeapObj * copy);
        //HeapObj(DataObject ** data, unsigned int size);
        long get_size();
        void dereference();
        void safe_dereference();
        inline void reference();
        DataObject * retrieve(unsigned int offset);
        inline void set(unsigned int offset, DataObject * value);
        void flatten();
        HeapObj * concat(HeapObj * lobj, long typeflag);
        HeapObj * alt_concat(HeapObj * lobj, long typeflag);

        inline void set_cast_type(int typeflag);
};

struct StackWrapper {
    std::vector<DataObject *> * params;
    unsigned int ip;
};

class ThreadMan {
    private:
        pthread_t thread;
    public:
        ThreadMan(void * (*context)(void *),
                  std::vector<DataObject *> * params,
                  unsigned int ip) {
            StackWrapper *s = new StackWrapper();
            s->params = params;
            s->ip = ip;
            pthread_create(&thread, NULL, context, (void *)s);
        }

        DataObject * join() {
            void * ret_uncast;
            pthread_join(thread, &ret_uncast);
            return (DataObject*)ret_uncast;
        }
};

#include "objects.cpp"
