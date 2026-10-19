import { resource } from '../../api/client'
import { Card, PageHeader, StatCard } from '../../components/ui'
import { useApi } from '../../hooks/useApi'
import { DataTable, results, StatusBadge } from '../_shared'

const productsApi = resource('products')
const kitsApi = resource('kits')
const shipmentsApi = resource('shipments')
const excursionsApi = resource('excursions')

export function InventoryPage() {
  const products = useApi(() => productsApi.list({ page_size: 30 }), [])
  const kits = useApi(() => kitsApi.list({ page_size: 80 }), [])
  const shipments = useApi(() => shipmentsApi.list({ page_size: 30 }), [])
  const excursions = useApi(() => excursionsApi.list({ page_size: 20 }), [])
  const kitRows = results(kits.data)

  return (
    <div className="tr-page">
      <PageHeader title="Investigational product" subtitle="Kits, shipments, accountability, expiry, and temperature excursions." />
      <div className="tr-grid-stats">
        <StatCard label="Products" value={results(products.data).length} />
        <StatCard label="Available kits" value={kitRows.filter((r) => (r as { status: string }).status === 'available').length} />
        <StatCard label="Dispensed" value={kitRows.filter((r) => (r as { status: string }).status === 'dispensed').length} />
        <StatCard label="Excursions" value={results(excursions.data).length} />
      </div>
      <Card title="Products">
        <DataTable loading={products.loading} rows={results(products.data)} empty="No products" columns={[{ key: 'code', label: 'Code' }, { key: 'name', label: 'Product' }, { key: 'strength', label: 'Strength' }, { key: 'storage_condition', label: 'Storage' }]} />
      </Card>
      <Card title="Kits">
        <DataTable loading={kits.loading} rows={kitRows} empty="No kits" columns={[{ key: 'kit_number', label: 'Kit' }, { key: 'product_name', label: 'Product' }, { key: 'lot_number', label: 'Lot' }, { key: 'expiry_date', label: 'Expiry' }, { key: 'status', label: 'Status', render: (r) => <StatusBadge value={String((r as { status: string }).status)} /> }]} />
      </Card>
      <Card title="Shipments">
        <DataTable loading={shipments.loading} rows={results(shipments.data)} empty="No shipments" columns={[{ key: 'reference', label: 'Shipment' }, { key: 'carrier', label: 'Carrier' }, { key: 'shipped_on', label: 'Shipped' }, { key: 'received_on', label: 'Received' }, { key: 'status', label: 'Status' }]} />
      </Card>
      <Card title="Temperature excursions">
        <DataTable loading={excursions.loading} rows={results(excursions.data)} empty="No excursions" columns={[{ key: 'recorded_at', label: 'When' }, { key: 'min_c', label: 'Min °C' }, { key: 'max_c', label: 'Max °C' }, { key: 'impact', label: 'Impact' }]} />
      </Card>
    </div>
  )
}
