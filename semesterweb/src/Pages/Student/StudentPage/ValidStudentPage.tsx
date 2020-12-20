import * as React from "react";

import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import { Dispatch } from "redux";
import { connect, ConnectedProps } from "react-redux";
import { makeStyles, Theme } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Fade from "@material-ui/core/Fade";
import { Redirect, useHistory } from "react-router";
import { getStudent } from "../../../Api/Student";
import { toggleLoading } from "../../../Store/System";
import LoadingCard from "../../CommonComponents/LoadingCard";
import HeaderCard from "../../CommonComponents/HeaderCard";
import TableCard from "../../CommonComponents/TableCard";
import { StudentReciept } from "../../../Objects/StudentReciept";

interface RouteParams {
  studentId: string;
}

function mapStateToDispatch(dispatch: Dispatch) {
  return {
    setLoading: () => {
      dispatch(toggleLoading());
    },
  };
}

const connector = connect(null, mapStateToDispatch);
type PropsFromRedux = ConnectedProps<typeof connector>;

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flex: 1,
    display: "flex",
    padding: theme.spacing(3),
    flexDirection: "column",
  },
  buttonDivision: {
    display: "flex",
    flex: 1,
    justifyContent: "space-evenly",
  },
}));

function ValidStudent({
  studentId,
  setLoading,
}: RouteParams & PropsFromRedux): JSX.Element {
  const classes = useStyles();
  const [isDataFetched, setDataFetched] = React.useState(false);
  const [data, setData] = React.useState<StudentReciept>(null);
  const history = useHistory();

  const fetchData = React.useCallback(async () => {
    setLoading();
    setDataFetched(false);
    const response = await getStudent(studentId);
    setData(response);
    setDataFetched(true);
    setLoading();
  }, [studentId, setLoading]);

  // Call Fetch to Execute
  React.useEffect(() => {
    fetchData();
  }, [studentId, fetchData]);

  const handleOnClickScores = () => {
    history.push(`/Student/Scores/${studentId}`);
  };

  const handleOnClickBacklogs = () => {
    history.push(`/Student/Scores/${studentId}`);
  };

  const handleOnClickBack = () => {
    history.push(`/Student`);
  };

  // If Data is fetched.
  if (isDataFetched && data !== null) {
    return (
      <div className={classes.root}>
        <HeaderCard content="Student Details" />
        <Fade in timeout={2500}>
          <TableCard data={data} alignment={["left", "right"]} />
        </Fade>
        <Fade in timeout={2500}>
          <Card elevation={5}>
            <CardContent>
              <div className={classes.buttonDivision}>
                <Button
                  color="secondary"
                  variant="outlined"
                  onClick={handleOnClickScores}
                >
                  View Student Scores
                </Button>
                <Button
                  color="secondary"
                  variant="outlined"
                  onClick={handleOnClickBacklogs}
                >
                  View Student Backlogs
                </Button>
                <Button
                  color="secondary"
                  variant="outlined"
                  onClick={handleOnClickBack}
                >
                  Go Back
                </Button>
              </div>
            </CardContent>
          </Card>
        </Fade>
      </div>
    );
  }

  if (isDataFetched && data === null) {
    return <Redirect to="/Student/NotFound" />;
  }

  return <LoadingCard />;
}

export default connector(ValidStudent);
