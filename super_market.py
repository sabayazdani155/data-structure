import random
from collections import deque

class Customer:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.remaining_service = service_time
        self.start_service_time = None   
        self.departure_time = None       


print("=== شبیه‌سازی صف صندوق فروشگاه ===\n")

num_checkouts = int(input("the number of checkouts(Checkout Lines): "))
sim_duration = int(input("مدت زمان شبیه‌سازی (دقیقه): "))
p = float(input("احتمال ورود مشتری در هر دقیقه (p بین 0 و 1): "))
min_service = int(input("حداقل زمان سرویس‌دهی (دقیقه): "))
max_service = int(input("حداکثر زمان سرویس‌دهی (دقیقه): "))



queues = [deque() for _ in range(num_checkouts)]
busy_times = [0] * num_checkouts

arrived_count = 0
served_count = 0
wait_times = []      # زمان انتظار در صف
system_times = []    # زمان کل در سیستم
max_queue_length = 0



for t in range(sim_duration):
    
    
    if random.random() < p:
        service_time = random.randint(min_service, max_service)
        customer = Customer(t, service_time)
        
        
        shortest_idx = min(range(num_checkouts), key=lambda i: len(queues[i]))
        queues[shortest_idx].append(customer)
        arrived_count += 1
    
    
    current_max = max(len(q) for q in queues)
    if current_max > max_queue_length:
        max_queue_length = current_max
    
    
    for i in range(num_checkouts):
        q = queues[i]
        if q:                                 
            busy_times[i] += 1                
            
            customer = q[0]
            
        
            if customer.start_service_time is None:
                customer.start_service_time = t
                wait_times.append(t - customer.arrival_time)
            
        
            customer.remaining_service -= 1
            
           
            if customer.remaining_service <= 0:
                customer.departure_time = t + 1
                system_times.append(customer.departure_time - customer.arrival_time)
                q.popleft()
                served_count += 1



avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
avg_system = sum(system_times) / len(system_times) if system_times else 0
utilization = (sum(busy_times) / (num_checkouts * sim_duration) * 100) if sim_duration > 0 else 0


print("\n" + "="*50)
print("          گزارش آماری شبیه‌سازی")
print("="*50)
print(f"تعداد مشتریان وارد شده       : {arrived_count}")
print(f"تعداد مشتریان سرویس‌دهی شده  : {served_count}")
print(f"متوسط زمان انتظار در صف       : {avg_wait:.2f} دقیقه")
print(f"متوسط زمان کل در سیستم        : {avg_system:.2f} دقیقه")
print(f"حداکثر طول صف مشاهده شده     : {max_queue_length} نفر")
print(f"میانگین بهره‌وری صندوق‌ها     : {utilization:.1f}%")
print("="*50)

if arrived_count > served_count:
    print(f"توجه: {arrived_count - served_count} مشتری هنوز در صف هستند (شبیه‌سازی تمام شد).")