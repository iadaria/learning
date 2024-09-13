function createSotre(reducer, initialState) {
  let currentReducer = reducer;
  let curentState = initialState;
  let listener = () => {};
  return {
    getState() {
      return curentState
    },
    dispath(action) {
      curentState = currentReducer(curentState, action);
      listener();
      return action;
    },
    subscribe(newListener) {
      listener = newListener;
    }
  }
}

function counterReducer(state = 0, action) {
  switch(action.type) {
    case 'INCREMENT':
      return state + 1;
    case 'DECREMENT':
      return state - 1;
    default:
      return state;
  }
}

let store = createSotre(counterReducer);

store.subscribe(() => console.log(store.getState()))

store.dispath({ type: 'INCREMENT'});
store.dispath({ type: 'INCREMENT'});
store.dispath({ type: 'DECREMENT'})