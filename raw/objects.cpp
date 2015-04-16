#include<algorithm>
#include<iostream>
#include<sstream>
#include<string>
#include<vector>

DataObject::DataObject(ObjectType new_type) {
    heap_offset = 0;
    type = new_type;
    switch(new_type) {
        case LONG:
            v_long = 0;
            break;
        case DOUBLE:
            v_double = 0;
            break;
        case STRING:
            v_string = new std::string("");
            break;
        case ARRAY:
            v_array = NULL;
            break;
    }
}
DataObject::DataObject(HeapObj * arr) {
    heap_offset = 0;
    v_array = arr;
    type = ARRAY;
}
DataObject::DataObject(const DataObject& copy) {
    heap_offset = 0;
    if(copy.type == LONG)
        v_long = copy.v_long;
    else if(copy.type == DOUBLE)
        v_double = copy.v_double;
    else if(copy.type == STRING) {
        v_string = new std::string(*copy.v_string);
    } else if(copy.type == ARRAY)
        v_array = copy.v_array;
    type = copy.type;
}

DataObject::~DataObject() {
    if(type == STRING)
        delete v_string;
    type = NONE;
}

DataObject * DataObject::set_type(ObjectType new_type) {
    if(new_type == type)
        return this;
    if(type == NONE)
        throw 1999;
    switch(new_type) {
        case LONG:
            if(type == DOUBLE) {
                type = new_type;
                v_long = (long)v_double;
            } else
                throw 2000;
            break;
        case DOUBLE:
            if(type == LONG) {
                type = new_type;
                v_double = (double)v_long;
            } else
                throw 2001;
           break;
        case STRING:
            std::stringstream strstream;
            if(type == LONG)
                strstream << v_long;
            else if(type == DOUBLE)
                strstream << v_double;
            else
                throw 2002;
            type = new_type;
            v_string = new std::string(strstream.str());
            break;
    }
    return this;
}

DataObject * DataObject::padd(long increment) {
    heap_offset += increment;
    return this;
}

long DataObject::get_long() const {
    long out = 0;
    if(type == LONG)
        out = v_long;
    else if(type == ARRAY)
        out = v_array->get_size();
    else {
        throw 1000;
    }

    delete this;
    return out;
}
long DataObject::get_size(bool destr, DataObject ** vm) const {
    long ret = 0;
    if(type == LONG)
        ret = vm[v_long - 1]->v_long;
    else if(type == ARRAY)
        ret = v_array->get_size();

    if(destr)
        delete this;
    return ret;
}
double DataObject::get_double() const {
    if(type != DOUBLE)
        throw 1001;
    double v = v_double;
    delete this;
    return v;
}
const std::string * DataObject::get_string() const {
    if(type != STRING)
        throw 1002;
    const std::string * v = new std::string(*v_string);
    delete this;
    return v;
}

inline DataObject * DataObject::retrieve(long offset, DataObject ** vm) {
    if(type == ARRAY)
        return v_array->retrieve(offset);
    else
        return vm[v_long + offset];
}

HeapObj * DataObject::get_heap_obj(DataObject ** vm) {
    HeapObj * ret;
    if(type == ARRAY)
        ret = v_array;
    else
        ret = new HeapObj(v_long, vm);

    delete this;
    return ret;
}

void DataObject::print() {
    safe_print();
    delete this;
}

inline void DataObject::safe_print() const {
    switch(type) {
        case LONG:
            std::cout << v_long;
            break;
        case DOUBLE:
            std::cout << v_double;
            break;
        case STRING:
            std::cout << *v_string;
            break;
    }
}


inline unsigned int get_rounded_size(unsigned int size) {
    if(size < 4) return 4;
    --size;
    size |= size >> 1;
    size |= size >> 2;
    size |= size >> 4;
    size |= size >> 8;
    size |= size >> 16;
    return ++size;
}


HeapObj::HeapObj(unsigned int size, int refcnt) {
    capacity = get_rounded_size(size);
    array = new DataObject*[capacity];
    cast_type = ALL;
    orig_size = size;
    refcount = refcnt;
    concats = NULL;
    ccount = 0;
    do_destroy = true;

    destructed = false;
}

HeapObj::HeapObj(unsigned int offset, DataObject ** vm) {
    unsigned int size = vm[offset - 1]->v_long;
    cast_type = ALL;
    orig_size = size;
    refcount = 0;
    concats = NULL;
    ccount = 0;
    do_destroy = false;

    array = new DataObject*[size];
    capacity = size;
    std::copy(vm + offset, vm + offset + size, array);

    destructed = false;
}

HeapObj::HeapObj(const HeapObj& copy) {
    //DEBUG//if(copy.destructed) throw 5000;

    array = new DataObject*[copy.capacity];
    capacity = copy.capacity;
    cast_type = copy.cast_type;
    orig_size = copy.orig_size;
    refcount = 1;
    concats = NULL;
    ccount = 0;
    do_destroy = true;

    if(copy.concats != NULL) {
        concats = new std::vector<HeapObj *>(*copy.concats);
        ccount = copy.ccount;
        for(int i = 0; i < ccount; ++i)
            (*concats)[i]->reference();
    }

    // Recursively copy a concatenated series of constructed arrays.
    for(int i = 0; i < orig_size; ++i)
        array[i] = new DataObject(*copy.array[i]);

    destructed = false;
}

HeapObj::HeapObj(HeapObj * copy) {
    //DEBUG//if(copy->destructed) throw 5000;

    if(copy->concats != NULL)
        copy->flatten();

    capacity = copy->capacity;
    array = new DataObject*[capacity];
    cast_type = copy->cast_type;
    orig_size = copy->orig_size;
    refcount = 1;
    concats = NULL;
    ccount = 0;
    do_destroy = true;

    // Recursively copy a concatenated series of constructed arrays.
    for(int i = 0; i < orig_size; ++i)
        array[i] = new DataObject(*copy->array[i]);

    destructed = false;
}
/*
HeapObj::HeapObj(DataObject ** data, unsigned int size) {
    array = new DataObject*[size];
    // We can copy the pointers directly because this reference will always
    // (or should always) be destroyed before the data is destroyed.
    for(unsigned int i = 0; i < size; i++)
        array[i] = data[i];
    orig_size = size;
    do_destroy = false;

    cast_type = ALL;
    refcount = 1;
    concats = NULL;
    ccount = 0;
    destructed = false;
}
*/

long HeapObj::get_size() {
    //DEBUG//if(destructed) throw 5000;
    unsigned int output = orig_size;
    if(concats != NULL) {
        for(int i = 0; i < ccount; ++i)
            output += (*concats)[i]->orig_size;
    }
    return output;
}

void HeapObj::dereference() {
    //debug//if(destructed) throw 5000;
    if(--refcount < 1) {
        // Drop the concatted arrays' refcounts.
        if(concats != NULL) {
            for(unsigned int i = 0; i < ccount; ++i)
                (*concats)[i]->dereference();
            delete concats;
        }

        // Delete all the referenced values.
        if(do_destroy)
            for(unsigned int i = 0; i < orig_size; ++i)
                delete array[i];
        delete[] array;

        // An hero.
        destructed = true;
        delete this;
    }
}

void HeapObj::safe_dereference() {
    if(--refcount < 1) {
        // Drop the concatted arrays' refcounts.
        if(concats != NULL) {
            for(unsigned int i = 0; i < ccount; ++i) {
                HeapObj * c = (*concats)[i];
                if(c->refcount == 0 && c->do_destroy)
                    continue;
                c->dereference();
            }
            delete concats;
        }

        delete[] array;
        delete this;
    }
}

inline void HeapObj::reference() {++refcount;}

DataObject * HeapObj::retrieve(unsigned int offset) {
    //DEBUG//if(destructed) throw 5000;
    if(ccount && offset >= orig_size) flatten();

    DataObject * ret = array[offset];

    if(cast_type != ALL && ret->type != cast_type)
        ret->set_type(cast_type);
    return ret;
}

inline void HeapObj::set(unsigned int offset, DataObject * value) {
    //DEBUG//if(destructed) throw 5000;
    if(offset >= orig_size)
        throw 3000;

    // We don't need to check that something's there or not because arrays
    // are immutable. The code generator would never give us an instruction
    // to overwrite a value in an array.
    // There's no need to make a copy of `value` because it would otherwise
    // have been destroyed, anyway.
    array[offset] = value;
}

void HeapObj::flatten() {
    //DEBUG//if(destructed) throw 5000;
    if(concats == NULL)
        return;

    unsigned int new_capacity = get_rounded_size(get_size());
    DataObject ** new_array;
    if(new_capacity > capacity) {
        new_array = new DataObject*[new_capacity];
        capacity = get_rounded_size(get_size());

        std::copy(array, array + orig_size, new_array);
        delete [] array;
    } else
        new_array = array;

    unsigned int counter = orig_size;
    for(unsigned int ci = 0; ci < ccount; ++ci) {
        HeapObj * tail = (*concats)[ci];
        if(tail->refcount > 1) {
            // If the refcount is 1, it's going to be destroyed either way.
            // Recycle the data objects if we can and do a safe dereference.
            // Otherwise, we don't need to dereference, we just need to
            // decrement the reference count.
            for(unsigned int i = 0; i < tail->orig_size; ++i) {
                new_array[counter] = new DataObject(*tail->array[i]);
                counter++;
            }
            tail->refcount -= 1;
            // The above line does this.
            //tail->dereference();
        } else {
            // Copy in the data objects.
            std::copy(tail->array, tail->array + tail->orig_size,
                      new_array + counter);
            // Update the counter.
            counter += tail->orig_size;
            // Kill the object softly with our song, kill it softly
            tail->safe_dereference();
        }
    }

    if(array != new_array)
        array = new_array;
    orig_size = counter;

    delete concats;
    concats = NULL;
    ccount = 0;
}

HeapObj * HeapObj::concat(HeapObj * robj, long typeflag) {
    //DEBUG//if(destructed || robj->destructed) throw 5000;

    if(robj->orig_size == 0 && robj->concats == NULL) {
        reference();
        set_cast_type(typeflag);
        return this;
    }
    if(orig_size == 0 && concats == NULL) {
        robj->reference();
        robj->set_cast_type(typeflag);
        return robj;
    }

    HeapObj * tcopy;
    if(concats != NULL) {
        tcopy = new HeapObj(orig_size, 1);
        for(unsigned int i = 0; i < orig_size; i++)
            tcopy->array[i] = new DataObject(*array[i]);

        tcopy->concats = new std::vector<HeapObj *>(*concats);
    } else {
        tcopy = new HeapObj(0, 1);
        tcopy->concats = new std::vector<HeapObj *>;
        tcopy->concats->push_back(this);

        reference();
    }

    // Copy the right array in.
    if(robj->orig_size) {
        tcopy->concats->push_back(robj);
        //robj->reference();
    }
    if(robj->concats != NULL)
        tcopy->concats->insert(tcopy->concats->end(),
                               robj->concats->begin(), robj->concats->end());

    tcopy->ccount = tcopy->concats->size();
    for(unsigned int i = 0; i < tcopy->ccount; i++)
        (*tcopy->concats)[i]->reference();

    // What should the cast type be?
    set_cast_type(typeflag);
    return tcopy;
}

HeapObj * HeapObj::alt_concat(HeapObj * robj, long typeflag) {
    if(refcount > 1 || robj->refcount > 1) {
        HeapObj * concatted = concat(robj, typeflag);

        // Drop the refcounts
        refcount -= 1;
        robj->refcount -= 1;

        return concatted;
    }

    if(robj->orig_size == 0 && robj->concats == NULL) {
        delete [] robj->array;
        delete robj;
        set_cast_type(typeflag);
        return this;
    } else if(orig_size == 0 && concats == NULL) {
        delete [] array;
        delete this;
        robj->set_cast_type(typeflag);
        return robj;
    }

    if(ccount || robj->ccount) {
        if(ccount == 0)
            concats = new std::vector<HeapObj *>;
        concats->push_back(robj);
        if(robj->ccount) {
            concats->insert(concats->end(),
                            robj->concats->begin(), robj->concats->end());
            delete robj->concats;
            robj->concats = NULL;
            robj->ccount = 0;
        }
        ccount = concats->size();
        return this;
    }

    DataObject ** temp;
    unsigned int new_len = orig_size + robj->orig_size;
    if(capacity < new_len) {
        unsigned int new_capacity = get_rounded_size(new_len);
        temp = new DataObject*[new_capacity];
        std::copy(array, array + orig_size, temp);
        capacity = new_capacity;
    } else
        temp = array;

    std::copy(robj->array, robj->array + robj->orig_size, temp + orig_size);

    delete [] array;
    array = temp;

    robj->safe_dereference();

    set_cast_type(typeflag);
    return this;
}

inline void HeapObj::set_cast_type(int typeflag) {
    if(typeflag < 0)
        cast_type = LONG;
    else if(typeflag > 0)
        cast_type = DOUBLE;
}
