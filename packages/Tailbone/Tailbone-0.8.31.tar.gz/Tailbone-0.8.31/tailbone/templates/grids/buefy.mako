## -*- coding: utf-8; -*-

<div id="buefy-table-app">
  <b-table
     :data="data"
     :columns="columns"
     :loading="loading"
     :row-class="getRowClass"

     :default-sort="[sortField, sortOrder]"
     backend-sorting
     @sort="onSort"

     % if grid.pageable:
     paginated
     :per-page="perPage"
     :current-page="page"
     backend-pagination
     :total="total"
     @page-change="onPageChange"
     % endif

     ## TODO: should let grid (or master view) decide how to set these?
     icon-pack="fas"
     ## note that :striped="true" was interfering with row status (e.g. warning) styles
     :striped="false"
     :hoverable="true"
     :narrowed="true">

    <template slot-scope="props">
      % for column in grid_columns:
          <b-table-column field="${column['field']}" label="${column['label']}" ${'sortable' if column['sortable'] else ''}>
            % if grid.is_linked(column['field']):
                <a :href="props.row._action_url_view" v-html="props.row.${column['field']}"></a>
            % else:
                {{ props.row.${column['field']} }}
            % endif
          </b-table-column>
      % endfor

      % if grid.main_actions or grid.more_actions:
          <b-table-column field="actions" label="Actions">
            % for action in grid.main_actions:
                <a :href="props.row._action_url_${action.key}"><i class="fas fa-${action.icon}"></i>
                  ${action.label}
                </a>
            % endfor
          </b-table-column>
      % endif
    </template>

    <template slot="empty">
      <section class="section">
        <div class="content has-text-grey has-text-centered">
          <p>
            <b-icon
               pack="fas"
               icon="fas fa-sad-tear"
               size="is-large">
            </b-icon>
          </p>
          <p>Nothing here.</p>
        </div>
      </section>
    </template>

    % if grid.pageable and grid.pager:
    <template slot="footer">
      <div class="has-text-right">showing {{ firstItem }} - {{ lastItem }} of {{ total }} results</div>
    </template>
    % endif

  </b-table>
</div>

<script type="text/javascript">

  new Vue({
      el: '#buefy-table-app',
      data() {
          return {
              data: ${json.dumps(grid_data['data'])|n},
              loading: false,
              sortField: '${grid.sortkey}',
              sortOrder: '${grid.sortdir}',
              rowStatusMap: ${json.dumps(grid_data['row_status_map'])|n},
              % if grid.pageable:
              % if static_data:
              total: ${len(grid_data['data'])},
              % else:
              total: ${grid_data['total_items']},
              % endif
              perPage: ${grid.pagesize},
              page: ${grid.page},
              firstItem: ${grid_data['first_item']},
              lastItem: ${grid_data['last_item']},
              % endif
          }
      },
      methods: {

          getRowClass(row, index) {
              return this.rowStatusMap[index]
          },

          loadAsyncData() {

              const params = [
                  'partial=true',
                  `sortkey=${'$'}{this.sortField}`,
                  `sortdir=${'$'}{this.sortOrder}`,
                  `pagesize=${'$'}{this.perPage}`,
                  `page=${'$'}{this.page}`
              ].join('&')

              this.loading = true
              this.$http.get(`${request.current_route_url(_query=None)}?${'$'}{params}`).then(({ data }) => {
                  this.data = data.data
                  this.rowStatusMap = data.row_status_map
                  this.total = data.total_items
                  this.firstItem = data.first_item
                  this.lastItem = data.last_item
                  this.loading = false
              })
              .catch((error) => {
                  this.data = []
                  this.total = 0
                  this.loading = false
                  throw error
              })
          },

          onPageChange(page) {
              this.page = page
              this.loadAsyncData()
          },

          onSort(field, order) {
              this.sortField = field
              this.sortOrder = order
              // always reset to first page when changing sort options
              // TODO: i mean..right? would we ever not want that?
              this.page = 1
              this.loadAsyncData()
          }
      }

  });

</script>
