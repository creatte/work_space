package main

import (
	"fmt"
)

//定义接口
type sorter interface{
        demo_sort(array []int,length int)
}

//归并排序结构体
type merges_sort struct{
}
//堆排序结构体
type heaps_sort struct{
}
//计数排序结构体
type counts_sort struct{
}

//归并排序
func (merge merges_sort) demo_sort(array []int,length int){
       merge_array := merge_sort(array,length)
       println_array(merge_array)
}

func merge_sort(array []int,length int) []int{
        if length < 2{
              return array  
        }
        mid := length/2
        left := array[0:mid]
        right := array[mid:]
        return merge(merge_sort(left,len(left)),merge_sort(right,len(right)))
}

func merge(left []int,right []int) []int{
        var result []int
        for len(left) != 0 && len(right) != 0 {
                if left[0] <= right[0] {
                        result = append(result, left[0])
                        left = left[1:]
                } else {
                        result = append(result, right[0])
                        right = right[1:]
                }
        }
        //当左边数组长度未到0时，全部放在result后面
        for len(left) != 0 {
                result = append(result, left[0])
                left = left[1:]
        }
        //当右边数组长度未到0时，全部放在result后面
        for len(right) != 0 {
                result = append(result, right[0])
                right = right[1:]
        }
        return result
}

//堆排序
func (heap heaps_sort) demo_sort(array []int,length int){
        heap_array := heap_sort(array,length)
        println_array(heap_array)
}

func heap_sort(array []int,length int) []int{
        build_Max_Heap(array, length)
        for i := length - 1; i >= 0; i-- {
                swap(array, 0, i)
                length -= 1
                heapify(array, 0, length)
        }
        return array
}

func build_Max_Heap(array []int,length int){
        for i := length / 2; i >= 0; i-- {
                heapify(array, i, length)
        }
}

func heapify(array []int, i int,length int){
        left := 2*i + 1
        right := 2*i + 2
        largest := i
        if left < length && array[left] > array[largest] {
                largest = left
        }
        if right < length && array[right] > array[largest] {
                largest = right
        }
        if largest != i {
                swap(array, i, largest)
                heapify(array, largest, length)
        }
}

func swap(array []int, i int, j int){
        array[i], array[j] = array[j], array[i]
}

//计数排序
func (count counts_sort) demo_sort(array []int,length int){
        count_array := count_sort(array,length)
        println_array(count_array)
}

func count_sort(array []int,length int) []int{
        max := find_max(array,length)  
        count_len := max + 1
        count_arr := make([]int,count_len)
        index := 0
        for i := 0; i < length; i++ {
                //统计array[i]的个数
                count_arr[array[i]] += 1
        }
        for j := 0; j < count_len; j++ {
                for count_arr[j] > 0 {
                        array[index] = j
                        index += 1
                        count_arr[j] -= 1
                }
        } 
        return array       
} 

//找到数组最大值
func find_max(array []int,length int) int{
        max := array[0]
        for i := 1 ; i < length; i++{
                if array[i] > max{
                        max = array[i]
                }
        }
        return max
}

//输出数组结果
func println_array(array []int){
        fmt.Println(array)
}

//构建一个策略模式
type sortselect struct{
        array []int
        selct sorter
}

func (s *sortselect) setarray(arr []int){
        s.array = arr
        fmt.Print("原来数组：")
        println_array(s.array)
}

func (s *sortselect) setselct(sel sorter){
        s.selct = sel
}

func (s *sortselect) demo_sort(){
        length := len(s.array)
        s.selct.demo_sort(s.array,length)
}

func main(){
        fmt.Println("第1组测试数据：")
        arr := []int{5,11,2,6,9,16,12,0}  
        sort := sortselect{}
        sort.setarray(arr)

        fmt.Print("归并排序:")
        sort.setselct(merges_sort{})
        sort.demo_sort()
        
        fmt.Print("计数排序：")
        sort.setselct(counts_sort{})
        sort.demo_sort()

        fmt.Print("堆排序")
        sort.setselct(heaps_sort{})
        sort.demo_sort()
        
        fmt.Println("第2组测试数据：")
        arr1 := []int{100,20,5,1,16,26,66,36}  
        sort1 := sortselect{}
        sort1.setarray(arr1)
        
        fmt.Print("归并排序:")
        sort1.setselct(merges_sort{})
        sort1.demo_sort()
        
        fmt.Print("计数排序：")
        sort1.setselct(counts_sort{})
        sort1.demo_sort()

        fmt.Print("堆排序")
        sort1.setselct(heaps_sort{})
        sort1.demo_sort()

        fmt.Println("第3组测试数据：")
        arr2 := []int{9,126,126,1,66,56,66,36}  
        sort2 := sortselect{}
        sort2.setarray(arr2)
        
        fmt.Print("归并排序:")
        sort2.setselct(merges_sort{})
        sort2.demo_sort()
        
        fmt.Print("计数排序：")
        sort2.setselct(counts_sort{})
        sort2.demo_sort()

        fmt.Print("堆排序")
        sort2.setselct(heaps_sort{})
        sort2.demo_sort()
}