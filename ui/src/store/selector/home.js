import { createSelector } from "reselect";

const selectHomeSlice = (state) => state.homeSlice;
const selectUserSlice = (state) => state.userSlice;

export const selectProjectAndAccountInfo = createSelector(
  [selectHomeSlice, selectUserSlice],
  (homeSlice, userSlice) => ({
    projectInfo: homeSlice.projectInfo,
    accountInfo: userSlice.accountInfo,
  })
);
