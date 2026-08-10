<template>
  <q-page class="q-pa-lg bg-grey-1">
    <div class="text-h5 text-weight-bolder q-mb-lg text-dark">Manage Users (Admin Only)</div>

    <!-- ตารางรายชื่อผู้ใช้งาน -->
    <q-card class="shadow-2 rounded-borders">
      <q-table
        :rows="users"
        :columns="columns"
        row-key="email"
        flat
      >
        <!-- Custom Column: Avatar & Name -->
        <template v-slot:body-cell-profile="props">
          <q-td :props="props">
            <q-item>
              <q-item-section avatar>
                <q-avatar size="40px"><img :src="props.row.avatar || 'https://cdn.quasar.dev/img/avatar.png'"></q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ props.row.name }}</q-item-label>
                <q-item-label caption>{{ props.row.email }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-td>
        </template>

        <!-- Custom Column: Actions (Edit / Delete) -->
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="q-gutter-sm">
            <!-- ปุ่มแก้ไข -->
            <q-btn round dense flat icon="edit" color="primary" @click="openEditDialog(props.row)">
              <q-tooltip>Edit Password & Avatar</q-tooltip>
            </q-btn>
            <!-- ปุ่มลบ (ซ่อนถ้าเป็นบัญชีตัวเอง) -->
            <q-btn v-if="props.row.email !== currentUserEmail" round dense flat icon="delete" color="red" @click="deleteUser(props.row.email)">
              <q-tooltip>Delete Account</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Dialog สำหรับแก้ไขรหัสผ่านและรูปโปรไฟล์ -->
    <q-dialog v-model="editDialog">
      <q-card style="min-width: 350px; border-radius: 12px;">
        <q-card-section>
          <div class="text-h6">Edit User Data</div>
          <div class="text-caption text-grey">Editing: {{ editingUser.email }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none q-gutter-y-md">
          <!-- เปลี่ยนรหัสผ่าน -->
          <div>
            <div class="text-weight-bold text-dark q-mb-xs">New Password</div>
            <q-input outlined dense v-model="editingUser.password" type="text" placeholder="Enter new password" />
          </div>
          <!-- เปลี่ยนรูปโปรไฟล์ -->
          <div>
            <div class="text-weight-bold text-dark q-mb-xs">Avatar URL</div>
            <q-input outlined dense v-model="editingUser.avatar" placeholder="https://..." />
            
            <!-- แสดงตัวอย่างรูปใหม่ -->
            <div class="q-mt-md text-center" v-if="editingUser.avatar">
              <q-avatar size="60px" class="shadow-2"><img :src="editingUser.avatar"></q-avatar>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup color="grey-7" />
          <q-btn flat label="Save Changes" @click="saveEdit" color="primary" class="text-weight-bold" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])
const currentUserEmail = ref('')
const editDialog = ref(false)
const editingUser = ref({ email: '', password: '', avatar: '' })

// คอลัมน์ของตาราง
const columns = [
  { name: 'profile', align: 'left', label: 'User Profile', field: 'name' },
  { name: 'role', align: 'left', label: 'Role', field: 'role' },
  { name: 'password', align: 'left', label: 'Password', field: 'password' },
  { name: 'actions', align: 'center', label: 'Actions' }
]

// โหลดข้อมูลผู้ใช้จาก localStorage ตอนเปิดหน้า
onMounted(() => {
  const storedUsers = JSON.parse(localStorage.getItem('appUsers')) || []
  users.value = storedUsers
  const me = JSON.parse(localStorage.getItem('user')) || {}
  currentUserEmail.value = me.email
})

// เปิดหน้าต่างแก้ไข
const openEditDialog = (user) => {
  editingUser.value = { ...user } // copy ข้อมูลมาใส่ฟอร์ม
  editDialog.value = true
}

// บันทึกการแก้ไข
const saveEdit = () => {
  const index = users.value.findIndex(u => u.email === editingUser.value.email)
  if (index !== -1) {
    users.value[index].password = editingUser.value.password
    users.value[index].avatar = editingUser.value.avatar
    // อัปเดตลงเครื่อง
    localStorage.setItem('appUsers', JSON.stringify(users.value))
    editDialog.value = false
  }
}

// ลบบัญชี
const deleteUser = (email) => {
  if (confirm(`Are you sure you want to delete ${email}?`)) {
    users.value = users.value.filter(u => u.email !== email)
    localStorage.setItem('appUsers', JSON.stringify(users.value))
  }
}
</script>