#include<string>
#include<vector>


inline DataObject * get_new_array(long size) {
    DataObject * new_arr = new DataObject(ARRAY);
    new_arr->v_array = new HeapObj(size, 1);
    return new_arr;
}

inline DataObject * new_long(long input) {
    DataObject * r = new DataObject(LONG);
    r->v_long = input;
    return r;
}

inline DataObject * new_double(double input) {
    DataObject * r = new DataObject(DOUBLE);
    r->v_double = input;
    return r;
}

inline DataObject * new_string(std::string * input) {
    DataObject * r = new DataObject(STRING);
    r->v_string = input;
    return r;
}

inline DataObject * pop_stack(std::vector<DataObject *> * data_stack) {
    DataObject * ret = data_stack->back();
    data_stack->pop_back();
    return ret;
}

inline void reference_do(DataObject * object) {
    if(object->type == ARRAY)
        object->v_array->reference();
}
inline void dereference_do(DataObject * object) {
    if(object->type == ARRAY)
        object->v_array->dereference();
}


// Debug Functions

void dump_stack(std::vector<DataObject *> * data_stack) {
    std::cout << "*************************" << std::endl;
    /*std::cout << LONG << " - long" << std::endl;
    std::cout << DOUBLE << " - double" << std::endl;
    std::cout << STRING << " - string" << std::endl;
    std::cout << NONE << " - gced" << std::endl;
    std::cout << ALL << " - all type" << std::endl;
    std::cout << ARRAY << " - array" << std::endl;*/
    std::cout << data_stack->size() << " stack items" << std::endl;
    for(int i = 0; i < data_stack->size(); i++) {
        DataObject * it = &*(data_stack->at(i));
        if(it->type == NONE) {
            std::cout << i << ": " << it << " gced" << std::endl;
            continue;
        }

        if(it->type != ARRAY) {
            std::cout << i << ": " << it << " ";
            switch(it->type) {
                case LONG:
                    std::cout << it->v_long;
                    break;
                case DOUBLE:
                    std::cout << it->v_double;
                    break;
                case STRING:
                    std::cout << *it->v_string;
                    break;
                default:
                    std::cout << "(" << it->type << ")";
            }
            std::cout << std::endl;
        } else {
            std::cout << i << ": " << it << " Array(" << it->v_array << "), orig_size=" << it->v_array->orig_size << ", size=" << it->v_array->get_size() << ", Refcount=" << it->v_array->refcount << ", HasNext=" << it->v_array->ccount << std::endl;
        }
    }
    std::cout << "*************************" << std::endl;
}

void print_ho(HeapObj * ho, bool flatten) {
    if(ho->ccount)
        std::cout << ho->ccount << " concatted arrays." << std::endl;
    if(ho->ccount && flatten)
        ho->flatten();
    for(int i = 0; i < ho->get_size(); i++) {
        DataObject * it = ho->retrieve(i);
        if(it->type == NONE) {
            std::cout << i << ": " << it << " GCed" << std::endl;
            continue;
        } else if(it->type == ARRAY) {
            std::cout << i << ": Nested arrays not yet supported." << std::endl;
            continue;
        }

        std::cout << i << ": " << it << " ";
        switch(it->type) {
            case LONG:
                std::cout << it->v_long;
                break;
            case DOUBLE:
                std::cout << it->v_double;
                break;
            case STRING:
                std::cout << *it->v_string;
                break;
        }
        std::cout << std::endl;
    }
}

void dump_offset(std::vector<DataObject *> * data_stack, long offset) {
    std::cout << "*************************" << std::endl;
    std::cout << "Inspecting stack offset " << offset << std::endl;
    DataObject * o = data_stack->at(offset);
    std::cout << "Address=" << o << std::endl;
    if(o->type != ARRAY) {
        std::cout << "Non-vector type found: " << o->type << std::endl;
    } else {
        HeapObj * oa = o->v_array;
        std::cout << "Heap Address=" << oa << std::endl;
        if(oa->get_size())
            print_ho(oa, false);
        else
            std::cout << "<no root elements>" << std::endl;

        if(oa->ccount) {
            std::cout << "Concats: " << oa->ccount << std::endl;
            for(unsigned int i = 0; i < oa->ccount; i++) {
                std::cout << "Concatted with " << oa->concats->at(i) << std::endl;
                print_ho(oa->concats->at(i), true);
            }
        }
    }
    std::cout << "*************************" << std::endl;
}

