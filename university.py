import csv
import os


class Student:
    def init(self, std_id, name, gpa):
        self.std_id = str(std_id).strip()
        self.name = str(name).strip()
        self.gpa = self._safe_float(gpa)

    @staticmethod
    def _safe_float(x, default=0.0):
        try:
            s = str(x).strip()
            if s == "":
                return default
            return float(s)
        except Exception:
            return default

    def str(self):
        return f"{self.name} (ID: {self.std_id}) - معدل: {self.gpa}"


class Professor:
    def init(self, name):
        self.name = str(name).strip()

    def str(self):
        return self.name


class Major:
    def init(self, name, total_area=0.0):
        self.name = str(name).strip()
        self.total_area = self._safe_float(total_area)
        self.students = LinkedList()      
        self.professors = LinkedList()    

    @staticmethod
    def _safe_float(x, default=0.0):
        try:
            s = str(x).strip()
            if s == "":
                return default
            return float(s)
        except Exception:
            return default



class Node:
    def init(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def init(self):
        self.head = None

    def clear(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def get_all(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

    def count(self):
        
        return len(self.get_all())

    def iter(self):
        current = self.head
        while current:
            yield current.data
            current = current.next



def _norm_key(k: str) -> str:
    
    return str(k).strip().lower().replace(" ", "").replace("-", "_")


def find_major(majors_ll, major_name):
    major_name = str(major_name).strip()
    for major in majors_ll:
        if major.name == major_name:
            return major
    return None


def _open_csv(path):
   
    return open(path, "r", encoding="utf-8-sig", newline="")


def _read_rows(path):
    with _open_csv(path) as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return [], []
      
        field_map = { _norm_key(fn): fn for fn in reader.fieldnames }
        rows = []
        for r in reader:
       
            nr = { _norm_key(k): (v if v is not None else "") for k, v in r.items() }
            rows.append(nr)
        return rows, list(field_map.keys())


def load_from_csv(majors_ll,
                  majors_file="majors.csv",
                  professors_file="professors.csv",
                  students_file="students.csv"):
    majors_ll.clear()

    missing = [p for p in (majors_file, professors_file, students_file) if not os.path.exists(p)]
    if missing:
        print("❌ این فایل‌ها پیدا نشدند:")
        for m in missing:
            print(f"   - {m}")
        print("✅ فایل‌ها باید کنار همین فایل .py باشند یا مسیر درست بدهی.")
        return

    
    rows, keys = _read_rows(majors_file)
    
    if "major_name" not in keys:
        print(f"❌ در {majors_file} ستون 'major_name' پیدا نشد. ستون‌های موجود: {keys}")
        return
    for row in rows:
        name = row.get("major_name", "").strip()
        if not name:
            continue
        area = row.get("total_area", 0)
        majors_ll.append(Major(name, area))

  
    rows, keys = _read_rows(professors_file)
   
    if "major" not in keys or "prof_name" not in keys:
        print(f"❌ در {professors_file} ستون‌های 'major' و/یا 'prof_name' پیدا نشد. ستون‌های موجود: {keys}")
        return

    for row in rows:
        major_name = row.get("major", "").strip()
        prof_name = row.get("prof_name", "").strip()
        if not major_name or not prof_name:
            continue
        major = find_major(majors_ll, major_name)
        if not major:
            major = Major(major_name)
            majors_ll.append(major)
        major.professors.append(Professor(prof_name))

    
    rows, keys = _read_rows(students_file)
 
    required = {"major", "student_id", "name", "gpa"}
    if not required.issubset(set(keys)):
        print(f"❌ در {students_file} ستون‌های لازم پیدا نشدند. لازم: {sorted(required)} | موجود: {keys}")
        return

    for row in rows:
        major_name = row.get("major", "").strip()
        if not major_name:
            continue
        major = find_major(majors_ll, major_name)
        if not major:
            major = Major(major_name)
            majors_ll.append(major)

        student = Student(
            row.get("student_id", ""),
            row.get("name", ""),
            row.get("gpa", 0)
        )
        major.students.append(student)

    print("✅ داده‌ها با موفقیت از فایل‌های CSV بارگذاری شدند.")



def show_student_count(majors_ll):
    print("\n📊 تعداد دانشجویان هر رشته:")
    for m in majors_ll:
        print(f"   {m.name}: {m.students.count()} دانشجو")


def show_top_3(majors_ll):
    print("\n🏆 ۳ دانشجوی برتر هر رشته (بر اساس معدل):")
    for m in majors_ll:
        print(f"\nرشته: {m.name}")
        students = m.students.get_all()
        if not students:
            print("   هیچ دانشجویی ثبت نشده")
            continue
        top3 = sorted(students, key=lambda s: s.gpa, reverse=True)[:3]
        for i, s in enumerate(top3, 1):
            print(f"   {i}. {s.name} → معدل {s.gpa}")


def show_average_gpa(majors_ll):
    print("\n📈 میانگین معدل دانشجویان هر رشته:")
    for m in majors_ll:
        students = m.students.get_all()
        if not students:
            print(f"   {m.name}: هیچ دانشجویی نیست")
            continue
        avg = sum(s.gpa for s in students) / len(students)
        print(f"   {m.name}: {avg:.2f}")


def show_professors_count(majors_ll):
    print("\n👨‍🏫 تعداد اساتید هر رشته:")
    for m in majors_ll:
        print(f"   {m.name}: {m.professors.count()} استاد")


def show_prof_to_major_ratio(majors_ll):
  
    print("\n⚖️ نسبت اساتید به هر رشته:")
    for m in majors_ll:
        
        print(f"   {m.name}: {m.professors.count()} استاد / ۱ رشته")


def show_space_per_student(majors_ll):
    print("\n🏢 فضای فیزیکی به ازای هر دانشجو (متر مربع):")
    for m in majors_ll:
        count = m.students.count()
        if count == 0:
            print(f"   {m.name}: هیچ دانشجویی نیست")
            continue
        space = m.total_area / count
        print(f"   {m.name}: {space:.2f} متر مربع")



def main():
    majors = LinkedList()
    print("🎓 سیستم مدیریت اطلاعات دانشگاه (با Linked List)")
    while True:
        print("\n" + "═" * 55)
        print("1. نمایش تعداد دانشجویان هر رشته")
        print("2. نمایش ۳ دانشجوی برتر هر رشته")
        print("3. نمایش میانگین معدل هر رشته")
        print("4. نمایش تعداد اساتید هر رشته")
        print("5. نمایش فضای فیزیکی به ازای هر دانشجو")
        print("6. بارگذاری اطلاعات از فایل CSV")
        print("7. نمایش نسبت اساتید به هر رشته")
        print("0. خروج")
        print("═" * 55)

        choice = input("گزینه خود را انتخاب کنید: ").strip()

        if choice == '1':
            show_student_count(majors)
        elif choice == '2':
            show_top_3(majors)
        elif choice == '3':
            show_average_gpa(majors)
        elif choice == '4':
            show_professors_count(majors)
        elif choice == '5':
            show_space_per_student(majors)
        elif choice == '6':
            load_from_csv(majors)
        elif choice == '7':
            show_prof_to_major_ratio(majors)
        elif choice == '0':
            print("👋 موفق باشی")
            break
        else:
            print("❌ گزینه نامعتبر است!")


if __name__ == "__main__":
    main()