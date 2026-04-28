# Chart Selection

## By relationship type

### Comparison
| Visual | When |
|---|---|
| Horizontal bar | Comparing categories, especially with long labels |
| Vertical column | Comparing categories with short labels, or time on x-axis |
| Bullet chart | KPI vs target with ranges |
| Dot plot | Precise value comparison without bar ink |

### Trend
| Visual | When |
|---|---|
| Line chart | Continuous time series, ≤6 series |
| Area chart | Cumulative or composition over time |
| Stepped line | Discrete state changes |
| Sparkline (in a card or table) | Inline trend indicator |

### Composition
| Visual | When |
|---|---|
| Stacked bar/column | Composition + comparison |
| 100% stacked bar | Percent breakdown across categories |
| Treemap | Hierarchical composition (e.g., category → subcategory) |
| Pie / donut | Only ≤5 parts, only when share-of-total is the message |
| Waterfall | Sequential additive changes |

### Distribution
| Visual | When |
|---|---|
| Histogram | Frequency distribution of a single measure |
| Box plot | Median + quartile + outliers across groups |
| Heat map | Density across two dimensions |

### Relationship / correlation
| Visual | When |
|---|---|
| Scatter | Two measures, optional category color |
| Bubble | Two measures + a size measure |
| Decomposition tree | Driver analysis (built-in AI visual) |
| Key influencers | Categorical attribution (built-in AI visual) |

### Geospatial
| Visual | When |
|---|---|
| Filled / shape map | Choropleth by region |
| ArcGIS / Azure Maps | Pin / heat / bubble by lat-long |
| Map (default) | Avoid except for quick prototyping |

### KPI / single value
| Visual | When |
|---|---|
| Card | One value, dominant emphasis |
| Multi-row card | 2–4 values |
| Gauge | Don't, unless target ranges are mandatory and audience expects it |
| KPI visual | Value + target + trend in one |

## Hard rules

- Don't use 3D anything. Reading angle distorts comparison.
- Don't combine more than two y-axis scales on one chart.
- Don't use rainbow palettes for sequential measures — use a single-hue gradient.
- Don't sort categorical bars alphabetically when there's a natural order (size, time, severity).
- Don't truncate the y-axis on a bar chart — it lies. Truncating a line chart can be acceptable with a clear axis label.
