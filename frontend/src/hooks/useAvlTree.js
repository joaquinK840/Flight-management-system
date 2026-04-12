import { useTreeOperations } from './useTreeOperations'
import { useTreeState } from './useTreeState'

const useAvlTree = () => {
    const state = useTreeState()
    const operations = useTreeOperations({ loadTree: state.loadTree })

    return {
        ...state,
        ...operations,
    }
}

export default useAvlTree
export { useTreeOperations, useTreeState }
