<template>
  <div id="first_search">
    <div v-if="!isLoading">
      https://github.com/<input type="text" v-model="username" />
      <div style="clear: both;"><br/></div>
      <button v-on:click="searchRepositories">Get repositories</button>

      <br/><br/><br/><br/>
      <p v-if="this.message.length" v-html="message"></p>
    </div>
    <div v-else>
      Getting repository list from Github...
    </div>

    <div v-show="showTable" id="table">
      <code>query: {{ query }}</code>
      <datatable v-bind="$data" />
    </div>

  </div>
</template>

<script>
import Operations from './components/'
export default {
  name: 'first_search',
  data () {
    return {
      username: 'kalkehcoisa',
      message: '',
      isLoading: false,

      columns: [
        { title: 'ID', field: 'id', visible: false },
        { title: 'Repository', field: 'name' },
        { title: 'Description', field: 'description', colStyle: 'max-width: 300px;' },
        { title: 'Language', field: 'language' },
        { title: 'Tags', field: 'tags', align: 'right', filterable: true, sortable: false },
        { title: 'Operations', tdComp: 'Operations', visible: 'true' }
      ],
      data: [],
      total: 0,
      query: {
        limit: 10
      },
      showTable: false,
    }
  },
  watch: {
    query: {
      handler (query) {
        // query: { "limit": 10, "offset": 0, "sort": "", "order": "" }
        if(this.refData) {
          this.data = this.refData.slice(query.offset, query.offset + query.limit);
          this.total = this.refData.length;
        }
      },
      deep: true
    }
  },

  methods: {
    searchRepositories: function() {
      if((this.username.length > 0) && !this.isLoading) {
        this.isLoading = true;
        this.$http.get('repositories/' + this.username)
          .then((response) => {
            this.refData = response.data;
            this.data = response.data.slice(0, 10);
            this.total = this.refData.length;

            this.isLoading = false;
            this.showTable = true;
          })
          .catch((response) => {
            if(response.status == 404) {
              this.message = 'Username [' + this.username + '] Not Found 404.' + 
                '<br/>Try another one.';
            } else {
              this.message = 'Unexpected error [' + response.status + '] happened: [' + response.statusText + ']';
            }
            this.isLoading = false;
          });
      }
    }
  },

  computed: {
    isLoaded: function() {
      if (this.message.length) {
        return true;
      }
      return false;
    }
  }

}
</script>

<style lang="scss">
@import '../node_modules/bootstrap/scss/bootstrap.scss';
$fa-font-path: "../node_modules/font-awesome/fonts";
@import '../node_modules/font-awesome/scss/font-awesome.scss';

div#first_search {
  max-width: 600px;
  text-align: center;
  margin: auto;
  margin-top: 30px;
}

div#table {
  max-width: 600px;
  text-align: center;
  margin: auto;
}
</style>
