import { useState } from 'react'
import type { Department } from '../types/clinic'
import useDepartments from '../hooks/useDepartments'
import './FilterPanel.css'

interface FilterPanelProps {
  selected: number[]
  onChange: (selected: number[]) => void
}

const COLUMN_SIZE = 22 // 左列に並べる件数（残りは右列）

function FilterPanel({ selected, onChange }: FilterPanelProps) {
  const { departments, loading, error } = useDepartments()
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

  // 左列・右列に分割（検索中はそのまま並べる）
  const isSearching = searchQuery.trim() !== ''
  const leftCol = isSearching ? filtered : filtered.slice(0, COLUMN_SIZE)
  const rightCol = isSearching ? [] : filtered.slice(COLUMN_SIZE)

  return (
    <aside className="filter-panel">
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
