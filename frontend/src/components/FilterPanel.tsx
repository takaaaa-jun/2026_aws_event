import { useState } from 'react'
import type { Department } from '../types/clinic'
import './FilterPanel.css'

interface FilterPanelProps {
  departments: Department[]   // App.tsx から受け取る
  loading: boolean
  error: string | null
  selected: number[]
  onChange: (selected: number[]) => void
  showDoctorlessArea: boolean
  onToggleDoctorlessArea: (checked: boolean) => void
}

const COLUMN_SIZE = 22 // 左列に並べる件数

function FilterPanel({
  departments,
  loading,
  error,
  selected,
  onChange,
  showDoctorlessArea,
  onToggleDoctorlessArea
}: FilterPanelProps) {
  const [searchQuery, setSearchQuery] = useState('')

  const toggle = (id: number) => {
    if (selected.includes(id)) {
      onChange(selected.filter((s) => s !== id))
    } else {
      onChange([...selected, id])
    }
  }

  const selectAll = () => onChange(departments.map((d: Department) => d.department_id))
  const clearAll = () => onChange([])

  // 検索でフィルタリング
  const filtered = departments.filter((d: Department) =>
    d.department_name.includes(searchQuery.trim())
  )

  // 左列・右列に分割
  const isSearching = searchQuery.trim() !== ''
  const leftCol = isSearching ? filtered : filtered.slice(0, COLUMN_SIZE)
  const rightCol = isSearching ? [] : filtered.slice(COLUMN_SIZE)

  return (
    <aside className="filter-panel">
      <h2 className="filter-title">マップ表示設定</h2>

      <div className="filter-setting-group">
        <label className="filter-label" style={{ fontWeight: 'bold', color: '#d32f2f' }}>
          <input
            type="checkbox"
            className="filter-checkbox"
            checked={showDoctorlessArea}
            onChange={(e) => onToggleDoctorlessArea(e.target.checked)}
          />
          無医地区を表示する
        </label>
      </div>

      <hr style={{ margin: '16px 0', border: 'none', borderTop: '1px solid #ccc' }} />

      <h2 className="filter-title">診療科で絞り込む</h2>

      {/* 検索ボックス */}
      <div className="filter-search-wrapper">
        <span className="filter-search-icon" aria-hidden="true">🔍</span>
        <input
          type="search"
          className="filter-search"
          placeholder="科名を検索..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* 選択中の科タグ */}
      {selected.length > 0 && (
        <div className="filter-tags">
          {selected.map((id) => {
            const dept = departments.find((d: Department) => d.department_id === id)
            if (!dept) return null
            return (
              <span key={id} className="filter-tag">
                {dept.department_name}
                <button
                  type="button"
                  className="filter-tag-remove"
                  onClick={() => toggle(id)}
                  aria-label={`${dept.department_name}を解除`}
                >
                  ×
                </button>
              </span>
            )
          })}
        </div>
      )}

      {/* ローディング中 */}
      {loading && (
        <p className="filter-status">読み込み中...</p>
      )}

      {/* エラー時 */}
      {error && (
        <p className="filter-status filter-error">{error}</p>
      )}

      {/* データ取得後 */}
      {!loading && !error && (
        <>
          <div className="filter-actions">
            <button type="button" className="filter-btn" onClick={selectAll}>
              すべて選択
            </button>
            <button type="button" className="filter-btn" onClick={clearAll}>
              クリア
            </button>
            {selected.length > 0 && (
              <span className="filter-count">{selected.length}科選択中</span>
            )}
          </div>

          {filtered.length === 0 ? (
            <p className="filter-status">「{searchQuery}」に一致する科がありません</p>
          ) : isSearching ? (
            // 検索中は1列で表示
            <ul className="filter-list filter-list--single">
              {filtered.map((department: Department) => (
                <li key={department.department_id} className="filter-item">
                  <label className="filter-label">
                    <input
                      type="checkbox"
                      className="filter-checkbox"
                      checked={selected.includes(department.department_id)}
                      onChange={() => toggle(department.department_id)}
                    />
                    {department.department_name}
                  </label>
                </li>
              ))}
            </ul>
          ) : (
            // 通常表示: 2列（左22・右21）
            <div className="filter-grid">
              <ul className="filter-list">
                {leftCol.map((department: Department) => (
                  <li key={department.department_id} className="filter-item">
                    <label className="filter-label">
                      <input
                        type="checkbox"
                        className="filter-checkbox"
                        checked={selected.includes(department.department_id)}
                        onChange={() => toggle(department.department_id)}
                      />
                      {department.department_name}
                    </label>
                  </li>
                ))}
              </ul>
              <ul className="filter-list">
                {rightCol.map((department: Department) => (
                  <li key={department.department_id} className="filter-item">
                    <label className="filter-label">
                      <input
                        type="checkbox"
                        className="filter-checkbox"
                        checked={selected.includes(department.department_id)}
                        onChange={() => toggle(department.department_id)}
                      />
                      {department.department_name}
                    </label>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </aside>
  )
}

export default FilterPanel
