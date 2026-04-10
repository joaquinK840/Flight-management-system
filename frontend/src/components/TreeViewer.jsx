
const nodeStyle = {
  padding: '12px 18px',
  margin: '6px 0',
  background: 'linear-gradient(135deg, #4B91FF 0%, #1A65D2 100%)',
  color: 'white',
  borderRadius: '32px',
  minWidth: '48px',
  textAlign: 'center',
  fontWeight: '700',
  boxShadow: '0 12px 24px rgba(0, 0, 0, 0.12)'
}

const containerStyle = {
  display: 'flex',
  justifyContent: 'center',
  fontFamily: 'Inter, system-ui, sans-serif',
  flexWrap: 'wrap'
}

const connectorLine = {
  width: '2px',
  height: '20px',
  backgroundColor: '#B0BEC5'
}

const childBlockStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  flex: 1,
  minWidth: '120px',
  margin: '0 8px'
}

const TreeViewer = ({ tree, title = "Estructura del Árbol AVL" }) => {
  const renderNode = (node) => {
    if (!node) {
      return <div style={{ flex: 1, minWidth: '120px' }} />
    }

    const hasChildren = node.left || node.right

    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: '120px' }}>
        <div style={nodeStyle}>{node.value}</div>

        {hasChildren && (
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', marginTop: '12px' }}>
            {renderChild(node.left)}
            {renderChild(node.right)}
          </div>
        )}
      </div>
    )
  }

  const renderChild = (child) => {
    if (!child) {
      return <div style={{ flex: 1, minWidth: '120px', margin: '0 8px' }} />
    }

    return (
      <div style={childBlockStyle}>
        <div style={connectorLine} />
        <div style={{ marginTop: '8px', width: '100%' }}>{renderNode(child)}</div>
      </div>
    )
  }

  return (
    <div
      style={{
        padding: '24px',
        backgroundColor: '#F4F7FC',
        borderRadius: '20px',
        marginTop: '20px',
        boxShadow: '0 20px 40px rgba(67, 89, 116, 0.12)'
      }}
    >
      <h2 style={{ margin: '0 0 18px', fontFamily: 'Inter, system-ui, sans-serif', color: '#1F304A' }}>
        {title}
      </h2>
      {tree ? (
        <div style={containerStyle}>{renderNode(tree)}</div>
      ) : (
        <p style={{ color: '#637381' }}>Árbol vacío - Inserta valores para comenzar</p>
      )}
    </div>
  )
}

export default TreeViewer
