#include<iostream>
#include<pthread.h>
#include<stack>
#include<stdlib.h>
#include<vector>

#include "objects.h"
#include "helpers.cpp"

using namespace std;

DataObject * run_context(vector<DataObject *> * data_stack_ref,
                         unsigned int ip);

void * bootstrap_context(void * stack_init) {
    StackWrapper * sw = (StackWrapper*)stack_init;

    // Cast everything and set up a return value
    vector<DataObject *> * stack_init_cast = sw->params;

    // Run the context
    DataObject * ret = run_context(stack_init_cast, sw->ip);
    // Return the output stack
    return (void *)ret;
}

DataObject ** virtual_memory;

DataObject * run_context(vector<DataObject *> * data_stack_ref,
                         unsigned int ip) {
    vector<DataObject *> * data_stack = new vector<DataObject *>;
    stack<int> frame_pointers;
    stack<int> instruction_pointers;
    
    if(data_stack_ref != NULL) {
        for(int i = 0; i < data_stack_ref->size(); i++)
            data_stack->push_back(&*data_stack_ref->at(i));
        delete data_stack_ref;
        frame_pointers.push(data_stack->size());
    } else {
        frame_pointers.push(0);
    }
    int fp_cache = frame_pointers.top();
    vector<ThreadMan *> threads;

%(instructions)s

    return NULL;
}

int main() {
    virtual_memory = new DataObject*[%(virtual_mem_size)d];
%(virtual_mem)s
    try {
        run_context(NULL, 0);
    } catch(int ex) {
        cout << "Program ended with exception " << ex << endl;
        return 1;
    }
    return 0;
}

