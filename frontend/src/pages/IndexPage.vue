<template>
  <q-page class="column items-center justify-evenly">
    <q-form class="column items-center q-gutter-md">
    <q-file
      v-model="file"
      label="Pick one file"
      filled 
      style="max-width: 300px"/>
    <q-btn @click="submit" label="Submit"/>
    </q-form>
    <div class="column items-center q-gutter-md">
      <q-btn @click="retrieve" label="Retrieve"/>
      <div>
        {{ statements }}
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: { },
  data () {
    const meta: Meta = {
      totalCount: 1200
    };
    return { 
      meta,
      file: ref(),
      statements: ref([])
     };
  },
  methods: {
    submit() {
      let formData = new FormData();
      formData.append("csv", this.file);
      const headers = {
        'Content-Type': 'multipart/form-data'
      }
      this.$api.post('statements', formData, {headers})
    },
    retrieve() {
      this.$api.get('statements')
      .then(statementsResponse => this.statements = statementsResponse.data)
    }
  }
});
</script>
