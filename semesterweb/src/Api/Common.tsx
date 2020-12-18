// I'm not sure what having multiple copies of the same statement is going to accomplish,
// so here is code to mitigate that.
import axios from "axios";
import Report from "../Objects/Report";

async function get<T>(url: string): Promise<T> {
  const response = await axios.get<T>(url);
  return response.data;
}

async function post<T extends Report<T>>(url: string, Obj: T): Promise<void> {
  const response = await axios.post(url, Obj.toObj());
  if (response.status !== 201) {
    throw new Error(
      `Returned StatusCode: ${response.status}|| ${response.statusText}`
    );
  }
}

const put = post;

export { get, post, put };
