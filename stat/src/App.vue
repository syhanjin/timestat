<script lang="ts" setup>
import { ref, nextTick } from 'vue'


interface Table {
  name: string
  rows: string[]
  columns: string[]
  data: Record<string, string[]>
}

const tables = ref<Table[]>([{
  name: '12周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '13周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '14周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '15周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '16周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '17周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}, {
  name: '18周',
  rows: ['12', '34', '56', '78'],
  columns: ['周一', '周二', '周三', '周四', '周五'],
  data: {}
}])

const b64 = ref(), b64_ref = ref()

async function submit() {
  const encodedText = encodeURIComponent(JSON.stringify(tables.value))
  b64.value = btoa(encodedText)
  await nextTick()
  b64_ref.value.textarea.select()

  await navigator.clipboard.writeText(b64.value)

  alert('已复制')
}

</script>

<template>
  <div class="container">
    <template v-for="table in tables" :key="table.name">
      <div class="table">
        <el-text>{{ table.name }}</el-text>
        <template v-for="row in table.rows" :key="row">
          <el-checkbox-group v-model="table.data[row]" class="row" size="small">
            <template v-for="column in table.columns" :key="column">
              <el-checkbox-button :value="column" class="column">
                {{ column }} {{ row }}
              </el-checkbox-button>
            </template>
          </el-checkbox-group>
        </template>
      </div>
    </template>
    <el-button @click="submit">提交</el-button>
    <el-input ref="b64_ref" v-model="b64" readonly type="textarea"></el-input>
  </div>
</template>

<style lang="scss" scoped>
.container {
  justify-content: center;
  margin: 30px 0;
  min-height: 800px;
  position: relative;
  width: 100%;
}

.table {
  padding: 1em;
}
</style>

